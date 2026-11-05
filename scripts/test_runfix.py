import copy,hashlib,json,os,subprocess,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace as A
from unittest.mock import patch
import requests
import da,cloud_transport as cloud,request_state as recovery,provider_state,transfer,browsing,save_watch

class Response:
 def __init__(self,events,status=200):self.events=events;self.status_code=status;self.headers={'X-Request-Id':'server-request'};self.closed=False
 def iter_lines(self,**kw):
  for x in self.events:
   if isinstance(x,Exception):raise x
   yield b'data: '+json.dumps(x).encode();yield b''
 def json(self):return {'error':{'code':'InvalidModel','message':'test'}}
 def close(self):self.closed=True

class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.w=Path(self.tmp.name).resolve();self.j=self.w/'out/jobs/job';self.j.mkdir(parents=True)
  self.limit={'id':'plan','new_usage':{'requests':4,'images':4,'audio_seconds':0}}
  self.charge={'requests':1,'images':1,'audio_seconds':0};self.ident={'stage':'vision','test':'identity'}
  cloud.configure({})
 def tearDown(self):self.tmp.cleanup();cloud.configure({})
 def pending(self):
  with self.assertRaises(TimeoutError):da.paid(self.w,self.j,self.ident,self.charge,lambda:(_ for _ in ()).throw(TimeoutError()),self.limit)
  return da.ledger(self.w)[0]['cache_id']
 def test_post_timeout_has_diagnostics_without_key(self):
  with patch.object(cloud.requests,'post',side_effect=requests.ReadTimeout()):
   with self.assertRaises(requests.ReadTimeout) as caught:cloud.response('https://example.invalid','private-secret','model',[])
  d=caught.exception.response_data
  self.assertEqual(d['diagnostics']['phase'],'waiting_response_headers');self.assertIsNone(d['diagnostics']['response_id'])
  self.assertNotIn('private-secret',json.dumps(d))
 def test_created_id_and_partial_text_survive_stream_failure(self):
  r=Response([{'type':'response.created','response':{'id':'resp-1','model':'actual'}},{'type':'response.output_text.delta','delta':'partial'},requests.ConnectionError()])
  with patch.object(cloud.requests,'post',return_value=r):
   with self.assertRaises(requests.ConnectionError) as caught:cloud.response('https://example.invalid','secret','model',[])
  self.assertEqual(caught.exception.response_data['diagnostics']['response_id'],'resp-1');self.assertTrue(r.closed)
 def test_complete_response_and_timeouts_are_transport_only(self):
  event={'type':'response.completed','response':{'id':'resp-1','model':'actual','status':'completed','usage':{'output_tokens':3},'output':[{'content':[{'type':'output_text','text':'complete'}]}]}}
  r=Response([event])
  cloud.configure({'VOLC_AGENT_READ_TIMEOUT':'350'})
  with patch.object(cloud.requests,'post',return_value=r) as post:
   result=cloud.response('https://example.invalid','secret','model',[],{'max_output_tokens':4096})
  self.assertEqual(post.call_args.kwargs['timeout'],(30,350));self.assertFalse(post.call_args.kwargs['json']['store']);self.assertEqual(result['text'],'complete')
  self.assertIsNotNone(result['diagnostics']['completed_seconds'])
 def test_incomplete_and_http_errors_never_become_success(self):
  for r in (Response([{'type':'response.incomplete','response':{'id':'r','status':'incomplete','output':[{'content':[{'type':'output_text','text':'partial'}]}]}}]),Response([],429)):
   with patch.object(cloud.requests,'post',return_value=r):
    with self.assertRaises(cloud.CloudError):cloud.response('https://example.invalid','secret','model',[])
   self.assertTrue(r.closed)
 def test_invalid_timeout_rejected(self):
  for value in ('nan','0','1801'):
   with self.assertRaises(ValueError):cloud.configure({'VOLC_AGENT_READ_TIMEOUT':value})
 def test_retry_retains_original_and_reuses_success(self):
  key=self.pending();original=copy.deepcopy(da.ledger(self.w)[0]);plan=recovery.retry(self.w,key)
  recovery.retry(self.w,key,plan['id'])
  result=da.paid(self.w,self.j,self.ident,self.charge,lambda:{'id':'new','text':'complete'},self.limit)
  self.assertEqual(da.ledger(self.w)[0],original);self.assertTrue((self.w/'cache'/f'{key}.pending.json').exists())
  self.assertEqual(len(da.ledger(self.w)),2);self.assertFalse(recovery.pending_for_job(self.w,'job'))
  self.assertEqual(da.paid(self.w,self.j,self.ident,self.charge,lambda:self.fail('duplicate network'),self.limit),result)
 def test_second_unknown_attempt_cannot_be_retried(self):
  key=self.pending();p=recovery.retry(self.w,key);recovery.retry(self.w,key,p['id'])
  with self.assertRaises(TimeoutError):da.paid(self.w,self.j,self.ident,self.charge,lambda:(_ for _ in ()).throw(TimeoutError()),self.limit)
  with self.assertRaisesRegex(ValueError,'One unresolved retry'):recovery.retry(self.w,key)
  self.assertEqual(len(recovery.pending_for_job(self.w,'job')),1)
 def test_reconciled_retry_reuses_child_without_third_submission(self):
  key=self.pending();p=recovery.retry(self.w,key);recovery.retry(self.w,key,p['id'])
  with self.assertRaises(TimeoutError):da.paid(self.w,self.j,self.ident,self.charge,lambda:(_ for _ in ()).throw(TimeoutError()),self.limit)
  child=da.ledger(self.w)[1]['cache_id'];da.write(self.w/'cache'/f'{child}.response.json',{'diagnostics':{'response_id':'known-child'},'response':{'id':'known-child','status':'completed','output':[{'content':[{'type':'output_text','text':'complete child'}]}]}})
  self.assertTrue(recovery.reconcile(self.w,child)['reconciled'])
  result=da.paid(self.w,self.j,self.ident,self.charge,lambda:self.fail('third submission'),self.limit)
  self.assertEqual(result['text'],'complete child');self.assertEqual(len(da.ledger(self.w)),2)
 def test_retry_alias_write_interruption_does_not_resubmit(self):
  key=self.pending();p=recovery.retry(self.w,key);recovery.retry(self.w,key,p['id'])
  with patch.object(recovery,'complete_retry',side_effect=OSError('interrupted alias')):
   with self.assertRaises(OSError):da.paid(self.w,self.j,self.ident,self.charge,lambda:{'id':'new','text':'complete'},self.limit)
  result=da.paid(self.w,self.j,self.ident,self.charge,lambda:self.fail('must reuse completed retry'),self.limit)
  self.assertEqual(result['id'],'new');self.assertEqual(len(da.ledger(self.w)),2)
 def test_reconcile_requires_matching_known_response_and_complete_output(self):
  key=self.pending();p=self.w/'cache'/f'{key}.response.json'
  data={'diagnostics':{'response_id':'known'},'response':{'id':'wrong','status':'completed','output':[{'content':[{'type':'output_text','text':'yes'}]}]}}
  da.write(p,data);self.assertFalse(recovery.reconcile(self.w,key)['reconciled'])
  data['response']['id']='known';da.write(p,data);self.assertTrue(recovery.reconcile(self.w,key)['reconciled'])
  self.assertEqual(da.ledger(self.w)[0]['status'],'unresolved');self.assertFalse(recovery.pending_for_job(self.w,'job'))
 def test_unknown_cache_hash_is_never_a_platform_id(self):
  key=self.pending();self.assertFalse(recovery.reconcile(self.w,key)['reconciled'])
  self.assertTrue(recovery.status(self.w,key)['requests'][0]['effective_blocking'])
 def test_reconcile_complete_cache_after_ledger_interruption(self):
  key=self.pending();before=copy.deepcopy(da.ledger(self.w))
  da.write(self.w/'cache'/f'{key}.json',{'id':'real-response','text':'complete','diagnostics':{'response_id':'real-response','phase':'completed'}})
  self.assertTrue(recovery.reconcile(self.w,key)['reconciled']);self.assertEqual(da.ledger(self.w),before)
  self.assertFalse(recovery.pending_for_job(self.w,'job'))
 def test_submission_intent_survives_interrupted_ledger_write(self):
  key=self.pending();(self.w/'requests.json').unlink()
  before=(self.w/'cache'/f'{key}.pending.json').read_bytes()
  rows=recovery.status(self.w,key)['requests'];self.assertEqual(len(rows),1);self.assertTrue(rows[0]['effective_blocking'])
  self.assertEqual((self.w/'cache'/f'{key}.pending.json').read_bytes(),before)
  with self.assertRaises(ValueError):da.paid(self.w,self.j,self.ident,self.charge,lambda:self.fail('duplicate'),self.limit)
 def test_complete_asr_cache_reconciles_after_ledger_interruption(self):
  self.ident={'stage':'asr','media':'sample'};key=self.pending()
  da.write(self.w/'cache'/f'{key}.json',{'log_id':'asr-platform-log','data':{'result':{'text':'','utterances':[]}},'diagnostics':{'phase':'completed','request_id':'asr-platform-log'}})
  self.assertTrue(recovery.reconcile(self.w,key)['reconciled']);self.assertEqual(da.ledger(self.w)[0]['status'],'unresolved')
 def test_unknown_work_does_not_block_another_job(self):
  self.pending();other=self.w/'out/jobs/other';other.mkdir()
  self.assertEqual(da.paid(self.w,other,{'stage':'vision','different':True},self.charge,lambda:{'text':'other complete'},self.limit)['text'],'other complete')
  self.assertTrue(recovery.pending_for_job(self.w,'job'))
 def test_pipeline_skips_unknown_work_and_visits_next_work(self):
  self.pending();da.write(self.j/'metadata.json',{'kind':'images'})
  other=self.w/'out/jobs/other';other.mkdir();da.write(other/'metadata.json',{'kind':'images'});da.write(other/'state.json',{'status':'completed'})
  plan={'jobs':[{'job':str(j.relative_to(self.w)),'metadata_hash':da.sha(j/'metadata.json')} for j in (self.j,other)]}
  plan['id']=da.digest(plan)[:24];path=self.w/'plan.json';da.write(path,plan)
  with patch.object(da,'config',return_value={'VOLC_AGENT_API_KEY':'fixture'}):result=da.run(self.w,A(plan=path,approve=plan['id']))
  self.assertEqual([x['status'] for x in result],['blocked','completed_cached'])
 def test_save_watch_missing_ambiguous_and_exact_owned_download(self):
  directory=self.w/'downloads';directory.mkdir();(directory/'user.txt').write_text('preserve')
  ident=save_watch.before(self.w,directory)['watch_id'];self.assertEqual(save_watch.after(self.w,ident)['status'],'not_observed')
  (directory/'a.mp4').write_bytes(b'new');(directory/'b.mp4').write_bytes(b'new')
  self.assertEqual(save_watch.after(self.w,ident)['status'],'ambiguous')
  result=save_watch.after(self.w,ident,'a.mp4',True)
  self.assertTrue(result['ownership_claimed']);self.assertTrue((directory/'user.txt').exists())
 def test_stage_options_are_distinct_from_timeout_settings(self):
  plan={'stage_response_options':{'vision':{'max_output_tokens':4096},'report':{'max_output_tokens':8192}}}
  self.assertEqual(da.stage_options(plan,'vision')['max_output_tokens'],4096)
  self.assertEqual(da.stage_options(plan,'report')['max_output_tokens'],8192)
 def test_abandon_keeps_ledger_and_preserves_import(self):
  key=self.pending();owned=self.j/'frame.jpg';owned.write_bytes(b'owned');original=self.w/'user.jpg';original.write_bytes(b'user')
  da.write(self.j/'ownership.json',[{'path':str(owned),'sha256':da.sha(owned),'kind':'derived'}]);da.write(self.j/'acquisition.json',{'preserved_imports':[{'path':str(original),'sha256':da.sha(original)}]})
  before=copy.deepcopy(da.ledger(self.w));job=recovery.abandon(self.w,key);self.assertFalse(da.clean_owned(self.w,job))
  self.assertTrue(original.exists());self.assertFalse(owned.exists());self.assertEqual(da.ledger(self.w),before)
 def test_inspect_abandon_preserves_session_input_and_other_requests(self):
  self.ident={'stage':'ui_vision','image':'one'};key=self.pending();before=copy.deepcopy(da.ledger(self.w))
  self.assertIsNone(recovery.abandon(self.w,key));self.assertEqual(da.ledger(self.w),before)
  self.assertFalse(recovery.blocking(self.w,da.ledger(self.w)[0]))
  with self.assertRaises(ValueError):recovery.retry(self.w,key)
  self.assertFalse((self.w/'out/jobs/job/abandoned.json').exists())
 def provider(self,url='https://example.org/parser',outcome='attempting'):
  return {'url':url,'host':'fixture','search_source':'https://example.org','round_id':'work-round','outcome':outcome}
 def test_batch_invalid_receipt_has_no_partial_commit(self):
  path=self.w/'batch.json';da.write(path,[self.provider(),self.provider('https://api.bilibili.com/')])
  with self.assertRaises(ValueError):da.provider(self.w,A(receipt=None,batch=path))
  self.assertFalse((self.w/'providers.json').exists());self.assertFalse((self.w/'provider-history.json').exists())
 def test_provider_transaction_replays_after_history_write_failure(self):
  apply=lambda a,b,c:da.provider_apply(self.w,a,b,c);original=provider_state.write
  def fail(path,value):
   if path.name=='provider-history.json':raise OSError('fixture interruption')
   return original(path,value)
  with patch.object(provider_state,'write',side_effect=fail):
   with self.assertRaises(OSError):provider_state.record(self.w,[self.provider()],apply)
  provider_state.recover(self.w)
  self.assertEqual(len(da.read(self.w/'provider-history.json')),1);self.assertFalse((self.w/'provider-transaction.json').exists())
 def test_routes_and_open_receipts_are_explicit(self):
  path=self.w/'p.json';da.write(path,self.provider());da.provider(self.w,A(receipt=path))
  result=da.provider(self.w,A(receipt=None,platform='douyin',round_id='work-round'))
  self.assertEqual(result['routes'][0]['url'],'https://snapany.com/zh/tiktok');self.assertEqual(result['remaining_sources'],2)
  self.assertEqual(len(result['unclosed_attempts']),1)
 def range_call(self,data,fail_once=False,bad=None):
  counts={}
  def call(url,out,hp,interval=None,validator=None,**kw):
   start,end=interval;counts[start]=counts.get(start,0)+1
   if fail_once and start>0 and counts[start]==1:return 35,0
   etag='"changed"' if bad=='changed' and start>0 else '"same"'
   status=200 if bad=='status' and start>0 else 206
   out.write_bytes(data[start:end+1]);hp.write_text(f'HTTP/1.1 {status} OK\nETag: {etag}\nContent-Range: bytes {start}-{end}/{len(data)}\n\n')
   return 0,status
  return call,counts
 def test_ranges_verify_intervals_and_retry_only_failed_segments(self):
  data=b'0123456789'*100;directory=self.w/'parts';directory.mkdir();call,counts=self.range_call(data,True)
  result=transfer.ranged('https://repo.anaconda.com/file',directory,hashlib.sha256(data).hexdigest(),8,call)
  self.assertEqual(result.read_bytes(),data);self.assertTrue(any(n==2 for n in counts.values()))
 def test_ranges_reject_changed_origin_wrong_status_and_wrong_digest(self):
  for index,bad in enumerate(('changed','status','hash')):
   directory=self.w/f'parts{index}';directory.mkdir();data=b'a'*100;call,_=self.range_call(data,bad=bad)
   with self.assertRaises(ValueError):transfer.ranged('https://repo.anaconda.com/file',directory,'0'*64 if bad=='hash' else hashlib.sha256(data).hexdigest(),4,call)
 def test_range_probe_rejects_unsupported_or_incorrect_interval(self):
  for n,(status,interval) in enumerate(((200,'bytes 0-0/100'),(206,'bytes 1-1/100'))):
   directory=self.w/f'probe{n}';directory.mkdir()
   def call(url,out,hp,*args,**kw):out.write_bytes(b'x');hp.write_text(f'HTTP/1.1 {status} OK\nETag: "same"\nContent-Range: {interval}\n\n');return 0,status
   with self.assertRaises(ValueError):transfer.ranged('https://repo.anaconda.com/file',directory,'a'*64,8,call)
 def test_range_segment_wrong_length_is_rejected(self):
  directory=self.w/'bad-length';directory.mkdir();data=b'x'*100;normal,_=self.range_call(data)
  def call(url,out,hp,interval=None,validator=None,**kw):
   result=normal(url,out,hp,interval,validator,**kw)
   if interval[0]>0:out.write_bytes(b'x')
   return result
  with self.assertRaisesRegex(ValueError,'length mismatch'):transfer.ranged('https://repo.anaconda.com/file',directory,hashlib.sha256(data).hexdigest(),4,call)
 def test_error_page_never_becomes_media_and_source_closes(self):
  path=self.w/'p.json';da.write(path,self.provider());da.provider(self.w,A(receipt=path))
  def call(url,out,hp,*args,**kw):out.write_bytes(b'<html>error</html>'.ljust(150,b' '));hp.write_text('HTTP/1.1 200 OK\n\n');return 0,200
  with self.assertRaises(OSError):transfer.download(self.w,'https://cdn.example.org/file','out/video.mp4',provider_receipt=path,kind='image',call=call)
  self.assertFalse((self.w/'out/video.mp4').exists());self.assertEqual(da.read(self.w/'providers.json')[0]['outcome'],'parsed_download_failed')
 def test_transfer_cleanup_preserves_changed_file(self):
  path=self.w/'p.json';da.write(path,self.provider());da.provider(self.w,A(receipt=path))
  from PIL import Image
  import io
  buf=io.BytesIO();Image.new('RGB',(10,10),'blue').save(buf,format='PNG')
  def call(url,out,hp,*args,**kw):out.write_bytes(buf.getvalue());hp.write_text('HTTP/1.1 200 OK\n\n');return 0,200
  result=transfer.download(self.w,'https://cdn.example.org/file','out/image.png',provider_receipt=path,kind='image',call=call)
  (self.w/'out/image.png').write_bytes(b'user changed')
  self.assertTrue(transfer.cleanup(self.w,result['id'])['cleanup_errors']);self.assertTrue((self.w/'out/image.png').exists())

if __name__=='__main__':unittest.main(verbosity=2)
