import unittest,tempfile,sys,json
from pathlib import Path
from types import SimpleNamespace as A
from unittest.mock import patch
from datetime import datetime,timezone,timedelta
import da
from PIL import Image

class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.w=Path(self.tmp.name); self.j=self.w/'out/jobs/test'; self.j.mkdir(parents=True)
  da.write(self.j/'metadata.json',{'schema_version':2,'kind':'images','duration':0})
  da.write(self.j/'ownership.json',[])
 def tearDown(self): self.tmp.cleanup()
 def owned(self):
  p=self.j/'work/f.jpg'; p.parent.mkdir(); Image.new('RGB',(32,32),'red').save(p); da.own(self.j,p); return p
 def text_results(self):
  (self.j/'analysis.md').write_text('Evidence frame f001; original media retired',encoding='utf-8'); da.write(self.j/'segments.json',[]); da.write(self.j/'understanding.json',[]); da.write(self.j/'review.json',{'status':'sampled','checks':[{'evidence':'mock','observation':'offline fixture'}],'analysis_sha256':da.sha(self.j/'analysis.md')})
 def test_finalize_and_validate_without_media(self):
  f=self.owned(); self.text_results(); r=da.finalize(self.w,A(job=self.j)); self.assertFalse(f.exists()); self.assertTrue(r['validation']['valid']); self.assertTrue(da.validate(self.j)['valid']); da.finalize(self.w,A(job=self.j))
 def test_owned_archive_cleanup_and_user_archive_preserved(self):
  src=self.w/'image.png'; Image.new('RGB',(32,32)).save(src)
  archive=self.w/'owned.zip'; archive.write_bytes(b'fixture')
  user=self.w/'user.zip'; user.write_bytes(b'keep')
  rec=self.w/'receipt.json'; da.write(rec,{'expected_images':1,'order_verified':True,'owned_artifacts':[{'path':str(archive),'sha256':da.sha(archive),'created_by_task':True}]})
  r=da.adopt(self.w,A(source=str(src),media=[src],receipt=rec,title='',author=''))
  self.assertFalse(da.clean_owned(self.w,Path(r['job'])))
  self.assertFalse(archive.exists()); self.assertTrue(user.exists()); self.assertTrue(src.exists())
 def test_changed_archive_rejected_before_adopt(self):
  src=self.w/'image.png'; Image.new('RGB',(32,32)).save(src)
  archive=self.w/'owned.zip'; archive.write_bytes(b'fixture')
  rec=self.w/'receipt.json'; da.write(rec,{'owned_artifacts':[{'path':str(archive),'sha256':'wrong','created_by_task':True}]})
  before=set((self.w/'out/jobs').iterdir())
  with self.assertRaises(ValueError): da.adopt(self.w,A(source=str(src),media=[src],receipt=rec,title='',author=''))
  self.assertEqual(before,set((self.w/'out/jobs').iterdir())); self.assertTrue(archive.exists())
 def test_review_required(self):
  f=self.owned()
  with self.assertRaises(ValueError): da.finalize(self.w,A(job=self.j))
  self.assertTrue(f.exists())
 def test_hash_change_preserved(self):
  f=self.owned(); f.write_bytes(b'changed'); self.assertTrue(da.clean_owned(self.w,self.j)); self.assertTrue(f.exists())
 def test_imported_original_preserved(self):
  src=self.w/'user.png'; Image.new('RGB',(32,32),'blue').save(src)
  r=da.adopt(self.w,A(source=str(src),media=[str(src)],receipt=None,title='',author='')); j=Path(r['job']); da.clean_owned(self.w,j); self.assertTrue(src.exists())
 def test_expiry_and_no_renewal(self):
  f=self.owned(); da.state(self.j,'failed'); first=da.read(self.j/'state.json')['expires_at']; da.state(self.j,'failed'); self.assertEqual(first,da.read(self.j/'state.json')['expires_at']); da.cleanup(self.w); self.assertTrue(f.exists())
  da.state(self.j,'failed',expires_at=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat()); da.cleanup(self.w); self.assertFalse(f.exists())
 def test_active_lock_skips_cleanup(self):
  f=self.owned(); da.state(self.j,'failed',expires_at='2000-01-01T00:00:00+00:00'); (self.w/'run.lock').write_text('lock'); da.cleanup(self.w); self.assertTrue(f.exists())
 def test_broken_links_and_embedded_media(self):
  self.text_results(); (self.j/'analysis.md').write_text('![x](work/x.jpg)'); da.write(self.j/'bad.json',{'x':'data:image/png;base64,xxx'}); self.assertEqual(len(da.validate(self.j)['errors']),2)
 def test_pending_and_cache(self):
  lim={'id':'a','new_usage':{'audio_seconds':0,'images':2,'requests':2}}; charge={'audio_seconds':0,'images':1,'requests':1}
  da.paid(self.w,self.j,{'id':1},charge,lambda:{'text':'yes'},lim)
  self.assertEqual(da.paid(self.w,self.j,{'id':1},charge,lambda:1/0,lim)['text'],'yes')
  with self.assertRaises(TimeoutError): da.paid(self.w,self.j,{'id':2},charge,lambda:(_ for _ in ()).throw(TimeoutError()),lim)
  with self.assertRaises(ValueError): da.paid(self.w,self.j,{'id':2},charge,lambda:None,lim)
  self.assertEqual(len(da.ledger(self.w)),2)
 def test_provider_success_requires_integrity(self):
  receipt=self.w/'r.json'; da.write(self.j/'integrity.json',{'status':'unknown'})
  da.write(receipt,{'url':'https://example.com/parse','host':'test','search_source':'https://example.com','outcome':'success','job':str(self.j)})
  with self.assertRaises(ValueError): da.provider(self.w,A(receipt=receipt))
  da.write(self.j/'integrity.json',{'status':'passed'}); da.provider(self.w,A(receipt=receipt)); self.assertEqual(len(da.provider(self.w,A(receipt=None))['providers']),1)
 def test_free_image_pipeline(self):
  src=self.w/'image.png'; Image.new('RGB',(64,64),'green').save(src); rec=self.w/'rec.json'; da.write(rec,{'expected_images':1,'order_verified':True})
  imported=da.adopt(self.w,A(source=str(src),media=[str(src)],receipt=rec,title='test',author='test')); j=Path(imported['job'])
  plan=da.preview(self.w,A(jobs=[j],question='test')); self.assertEqual(plan['new_usage']['requests'],2)
  args=A(plan=self.w/'out/plans'/f"{plan['id']}.json",approve=plan['id'])
  with patch.dict('os.environ',{'VOLC_AGENT_API_KEY':'mock'}),patch.object(da,'response',return_value={'id':'mock','text':'Evidence f00001','usage':{}}) as mock:
   da.run(self.w,args); self.assertEqual(mock.call_count,2)
   da.state(j,'failed'); da.clean_owned(self.w,j); (j/'analysis.md').unlink(); da.run(self.w,args); self.assertEqual(mock.call_count,2)
   da.write(j/'review.json',{'status':'sampled','checks':[{'evidence':'mock','observation':'offline fixture'}],'analysis_sha256':da.sha(j/'analysis.md')}); da.finalize(self.w,A(job=j)); da.run(self.w,args); self.assertEqual(mock.call_count,2)
  self.assertTrue(src.exists()); self.assertFalse(any(p.suffix in da.MEDIA for p in j.rglob('*') if p.is_file()))
 def test_migration_preserves_submissions(self):
  da.write(self.j/'metadata.json',{'schema_version':1,'kind':'images','duration':0}); self.owned(); self.text_results(); (self.j/'subtitles.srt').write_text('native')
  record={'cache_id':'old','charge':{'requests':1,'images':0,'audio_seconds':0},'status':'submitted'}; (self.w/'requests.jsonl').write_text(json.dumps(record)+'\n')
  self.assertEqual(da.migrate(self.w)['requests'],1); da.migrate(self.w,True); self.assertEqual(da.ledger(self.w),[record]); self.assertFalse((self.j/'subtitles.srt').exists()); self.assertTrue((self.j/'subtitles.srt.json').exists())
 def test_wrong_identity_rejected(self):
  src=self.w/'image.png'; Image.new('RGB',(32,32)).save(src); r=self.w/'receipt.json'; da.write(r,{'source_id':'wrong'})
  with self.assertRaises(ValueError): da.adopt(self.w,A(source=str(src),media=[str(src)],receipt=r,title='',author=''))
 def test_sampling_short_dense_long_sparse(self):
  self.assertLess(da.sampling_interval(8),da.sampling_interval(484)); self.assertLess(da.sampling_interval(484),da.sampling_interval(7200))
 def test_external_path_tamper_preserves_file(self):
  p=self.w/'user.txt'; p.write_text('keep'); da.write(self.j/'acquisition.json',{'owned_downloads':[]}); da.write(self.j/'ownership.json',[{'path':str(p),'sha256':da.sha(p),'kind':'browser_download'}]); self.assertTrue(da.clean_owned(self.w,self.j)); self.assertTrue(p.exists())
 def test_cleanup_interrupt_and_retry(self):
  p=self.owned(); original=Path.unlink
  def locked(path,*a,**k):
   if path==p: raise PermissionError('file occupied')
   return original(path,*a,**k)
  with patch.object(Path,'unlink',locked): self.assertTrue(da.clean_owned(self.w,self.j))
  self.assertTrue(p.exists()); self.assertFalse(da.clean_owned(self.w,self.j)); self.assertFalse(p.exists())
 def test_expired_media_does_not_release_pending(self):
  self.owned(); da.state(self.j,'failed',expires_at='2000-01-01T00:00:00+00:00'); da.write(self.w/'cache/x.pending.json',{'job':self.j.name,'charge':{'requests':1}}); da.cleanup(self.w); self.assertTrue((self.w/'cache/x.pending.json').exists())
 def test_stray_binary_prevents_completed(self):
  self.owned(); self.text_results(); (self.j/'unknown.bin').write_bytes(b'owned?'); da.finalize(self.w,A(job=self.j)); self.assertEqual(da.read(self.j/'state.json')['status'],'cleanup_pending')
 def test_cleaned_preview_needs_no_media(self):
  self.owned(); self.text_results(); da.finalize(self.w,A(job=self.j)); p=da.preview(self.w,A(jobs=[self.j],question='cached')); self.assertEqual(p['new_usage']['requests'],0)
 def test_truncated_video_rejected(self):
  video=self.w/'short.mp4'; da.core.command(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=64x64:d=1','-c:v','libx264',video]); rec=self.w/'r.json'; da.write(rec,{'identity_verified':True,'page_duration':30,'head_tail_verified':True})
  result=da.adopt(self.w,A(source='https://www.douyin.com/video/123456789',media=[video],receipt=rec,title='',author='')); self.assertIn('duration_mismatch',result['integrity']['errors'])
 def test_full_silent_video_no_audio(self):
  video=self.w/'silent.mp4'; da.core.command(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=64x64:d=1','-c:v','libx264',video]); rec=self.w/'r.json'; da.write(rec,{'identity_verified':True,'page_duration':1,'head_tail_verified':True})
  result=da.adopt(self.w,A(source=str(video),media=[video],receipt=rec,title='',author='')); p=da.preview(self.w,A(jobs=[Path(result['job'])],question='test')); self.assertEqual(p['new_usage']['audio_seconds'],0)
 def test_provider_limit_and_failure_history(self):
  r=self.w/'provider.json'
  for i in range(3):
   da.write(r,{'url':f'https://example{i}.org','host':'test','search_source':'https://example.org','outcome':'unavailable','round_id':'r1'}); da.provider(self.w,A(receipt=r))
  da.write(r,{'url':'https://example4.org','host':'test','search_source':'https://example.org','outcome':'login_required','round_id':'r1'})
  with self.assertRaises(ValueError): da.provider(self.w,A(receipt=r))
  x=da.read(r); x['round_id']='r2'; da.write(r,x); da.provider(self.w,A(receipt=r)); self.assertEqual(len(da.read(self.w/'provider-history.json')),4)
 def test_preview_duplicate_jobs(self):
  self.text_results(); da.state(self.j,'completed'); m=da.read(self.j/'metadata.json'); m['media_identity']='same'; da.write(self.j/'metadata.json',m); p=da.preview(self.w,A(jobs=[self.j,self.j],question='same')); self.assertEqual(len(p['jobs']),1); self.assertEqual(len(p['duplicates_skipped']),1)
 def test_native_offset_long_audio(self):
  video=self.w/'long.mp4'; da.core.command(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=64x64:r=1:d=301','-f','lavfi','-i','sine=frequency=300:duration=301','-c:v','libx264','-c:a','aac','-shortest',video])
  rec=self.w/'r.json'; da.write(rec,{'identity_verified':True,'page_duration':301,'head_tail_verified':True}); j=Path(da.adopt(self.w,A(source=str(video),media=[video],receipt=rec,title='',author=''))['job'])
  frame=j/'work/f.jpg'; Image.new('RGB',(32,32)).save(frame); da.own(j,frame); rows=[{'id':'f1','time':0,'index':1,'path':'work/f.jpg','sha256':da.sha(frame)}]
  with patch.object(da,'sample',return_value=rows): p=da.preview(self.w,A(jobs=[j],question='test'))
  self.assertEqual(len(p['jobs'][0]['chunks']),2); self.assertAlmostEqual(p['new_usage']['audio_seconds'],301,places=1)
  async def recognize(*a): return {'data':{'result':{'utterances':[{'start_time':100,'end_time':500,'text':'test'}]}}}
  with patch.dict('os.environ',{'VOLC_AGENT_API_KEY':'mock'}),patch.object(da,'recognize',recognize),patch.object(da,'response',return_value={'text':'f1 test'}): da.run(self.w,A(plan=self.w/'out/plans'/f"{p['id']}.json",approve=p['id']))
  segments=da.read(j/'segments.json'); self.assertEqual(segments[1]['start'],300.1); self.assertEqual(segments[1]['native']['start_time'],100)
 @unittest.skipUnless(sys.platform=='win32','Windows file sharing test')
 def test_real_windows_file_lock(self):
  import ctypes
  from ctypes import wintypes
  p=self.owned(); k=ctypes.WinDLL('kernel32',use_last_error=True); k.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]; k.CreateFileW.restype=wintypes.HANDLE; k.CloseHandle.argtypes=[wintypes.HANDLE]
  handle=k.CreateFileW(str(p),0x80000000,0,None,3,128,None); self.assertNotEqual(handle,ctypes.c_void_p(-1).value)
  try: self.assertTrue(da.clean_owned(self.w,self.j)); self.assertTrue(p.exists())
  finally: k.CloseHandle(handle)
  self.assertFalse(da.clean_owned(self.w,self.j)); self.assertFalse(p.exists())
 def test_dead_owner_token_recovers_without_early_deletion(self):
  import os
  p=self.owned(); da.state(self.j,'processing'); da.write(self.w/'run.lock',{'pid':os.getpid(),'process_token':'previous-incarnation'})
  da.cleanup(self.w); self.assertFalse((self.w/'run.lock').exists()); self.assertEqual(da.read(self.j/'state.json')['status'],'interrupted'); self.assertTrue(p.exists())
 def test_untimed_recognition_remains_text(self):
  m={'schema_version':2,'source':{'kind':'local','id':'test'},'media_identity':'untimed','kind':'video','has_audio':True,'duration':1}; da.write(self.j/'metadata.json',m)
  da.write(self.w/'cache'/f'{da.digest(da.asr_identity(m))}.json',{'data':{'result':{'text':'recognized without timing'}}})
  p={'model':'mock','question':'test','jobs':[{'job':str(self.j.relative_to(self.w)),'metadata_hash':da.sha(self.j/'metadata.json'),'asr_cached':True,'chunks':[],'groups':[]}],'new_usage':{'audio_seconds':0,'images':0,'requests':1}}; p['id']=da.digest(p)[:24]; path=self.w/'plan.json'; da.write(path,p)
  with patch.dict('os.environ',{'VOLC_AGENT_API_KEY':'mock'}),patch.object(da,'response',return_value={'text':'No reliable timing'}) as call:
   da.run(self.w,A(plan=path,approve=p['id'])); prompt=call.call_args.args[2][0]['text']; self.assertIn('recognized without timing',prompt); self.assertIn('missing native speech timestamps',prompt)
  self.assertEqual(da.read(self.j/'segments.json'),[]); self.assertTrue(da.read(self.j/'transcript.json')['missing_timing'])
 def test_invalid_receipt_leaves_no_copied_media(self):
  src=self.w/'source.png'; Image.new('RGB',(32,32),'red').save(src)
  r=self.w/'bad-receipt.json'; da.write(r,{'owned_downloads':[{'path':str(src),'sha256':'wrong','created_by_task':True}]})
  before=set((self.w/'out/jobs').iterdir())
  with self.assertRaises(ValueError): da.adopt(self.w,A(source=str(src),media=[str(src)],receipt=str(r),title='',author=''))
  self.assertEqual(before,set((self.w/'out/jobs').iterdir())); self.assertTrue(src.exists())
if __name__=='__main__': unittest.main(verbosity=2)
