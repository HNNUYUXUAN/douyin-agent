import unittest,tempfile,json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import browsing as b
import da
from legacy import source,write,read

class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.w=Path(self.tmp.name).resolve()
  self.c={'platforms':['douyin','youtube'],'mode':'selective','entry':'recommendations','selection':'user marked', 'max_seconds':600,'max_items':2,'image_dwell_seconds':3,'limits':{'requests':2,'images':2,'audio_seconds':0,'search_requests':0}}
 def tearDown(self):self.tmp.cleanup()
 def active(self):
  s=b.create(self.w,self.c);b.change(self.w,s['id'],'approve',s['approval_id']);return s
 def test_modes_and_explicit_limits(self):
  for field in ('mode','limits','entry'):
   c=dict(self.c);c.pop(field)
   with self.assertRaises(ValueError):b.create(self.w,c)
  self.c['max_items']=None;self.c['max_seconds']=None
  with self.assertRaises(ValueError):b.create(self.w,self.c)
 def test_approval_tamper_and_pause(self):
  s=b.create(self.w,self.c)
  with self.assertRaises(ValueError):b.load(self.w,s['id'],True)
  with self.assertRaises(ValueError):b.change(self.w,s['id'],'approve','wrong')
  b.change(self.w,s['id'],'approve',s['approval_id']);b.change(self.w,s['id'],'pause')
  with self.assertRaises(ValueError):b.check(self.w,s['id'],{},[])
  b.change(self.w,s['id'],'resume',s['approval_id'])
  p,d=b.load(self.w,s['id']);d['config']['limits']['requests']=999;write(p/'session.json',d)
  with self.assertRaisesRegex(ValueError,'changed'):b.load(self.w,s['id'])
 def test_budget_reserves_failures(self):
  s=self.active();records=[{'session_id':s['id'],'charge':{'requests':2},'status':'completed'}]
  with self.assertRaisesRegex(ValueError,'budget'):b.check(self.w,s['id'],{'requests':1},records)
  records[0]['status']='unresolved'
  with self.assertRaisesRegex(ValueError,'Unresolved'):b.check(self.w,s['id'],{},records)
 def test_playback_requires_actual_elapsed_and_defer_continues(self):
  s=self.active();url='https://youtu.be/abcdefghijk'
  item={'source':url,'status':'played','playback':{'muted':True,'rate':1,'seeked':False,'duration':30,'start':0,'end':30,'elapsed_seconds':1}}
  with self.assertRaises(ValueError):b.record(self.w,s['id'],item)
  b.record(self.w,s['id'],{'source':url,'status':'deferred','reason':'download blocked'})
  b.record(self.w,s['id'],{'source':'https://youtu.be/lmnopqrstuv','status':'observed'})
  self.assertEqual(len(b.load(self.w,s['id'])[1]['items']),2)
 def test_browse_cannot_authorize_content(self):
  self.c['mode']='browse';s=self.active()
  with self.assertRaises(ValueError):b.check(self.w,s['id'],{},[],'report')
 def test_selective_job_needs_selection(self):
  s=self.active();url='https://youtu.be/abcdefghijk';b.record(self.w,s['id'],{'source':url,'status':'observed'})
  with self.assertRaises(ValueError):b.scope_job(self.w,s['id'],{'source':source(url)},[])
 def test_paid_session_limits_and_cache(self):
  s=self.active();p=b.root(self.w,s['id']);limit={'id':'test','session_id':s['id'],'new_usage':self.c['limits']};charge={'requests':1,'images':1,'audio_seconds':0}
  for i in range(2):da.paid(self.w,p,{'stage':'ui_vision','i':i},charge,lambda:{'text':'ok'},limit)
  with self.assertRaises(ValueError):da.paid(self.w,p,{'stage':'ui_vision','i':3},charge,lambda:self.fail('over budget'),limit)
  self.assertEqual(da.paid(self.w,p,{'stage':'ui_vision','i':0},charge,lambda:self.fail('cache missed'),limit)['text'],'ok')
 def test_platforms_and_signed_parameter_removal(self):
  cases=[('https://youtu.be/abcdefghijk?si=secret','youtube'),('https://www.xiaohongshu.com/explore/0123456789abcdef01234567?xsec_token=secret','xiaohongshu'),('https://www.tiktok.com/@example/video/7581709508896984366','tiktok'),('https://www.douyin.com/video/7581709508896984366','douyin')]
  for url,p in cases:
   x=source(url);self.assertEqual(x['platform'],p);self.assertNotIn('secret',json.dumps(x))
  for host in ('v.douyin.com','vm.tiktok.com','xhslink.com','xhslink.cn'):self.assertEqual(source('https://'+host+'/abc')['kind'],'unresolved')
  with self.assertRaises(ValueError):source('https://www.youtube.com.evil.test/watch?v=abcdefghijk')
 def test_prefixed_knowledge_evidence(self):
  import knowledge as k
  write(self.w/'proof.json',{})
  data={'id':'prefixed','title':'Test','symptom':'Issue','action':'Fixed','result':'Observed','verification':'Synthetic','keywords':['test'],'sources':['workspace:proof.json']}
  write(self.w/'input.json',data);r=k.record(self.w,self.w/'input.json');self.assertIn('workspace:proof.json',Path(r['case']).read_text(encoding='utf-8'))
 def test_inspect_fenced_json_preserves_input_and_counts_charge(self):
  from PIL import Image
  self.c['mode']='browse';s=self.active();p=self.w/'page.png';Image.new('RGB',(32,32)).save(p)
  a=SimpleNamespace(session=s['id'],image=str(p),snapshot='original-snapshot',goal='Find mute')
  payload={'observation':'Paused','candidates':[{'label':'Mute','location_basis':'visible speaker'}],'uncertainty':'Host verification required'}
  result=b.inspect(self.w,a,da.paid,da.ledger,lambda w:{'VOLC_AGENT_API_KEY':'synthetic-test-key'},lambda *args:{'text':'```json\n'+json.dumps(payload)+'\n```'})
  self.assertTrue(p.exists());self.assertEqual(result['snapshot'],'original-snapshot');self.assertEqual(b.usage(da.ledger(self.w),s['id'])['requests'],1)
  b.inspect(self.w,a,da.paid,da.ledger,lambda w:{'VOLC_AGENT_API_KEY':'synthetic-test-key'},lambda *args:self.fail('cached response should not resubmit'))
  self.assertEqual(b.usage(da.ledger(self.w),s['id'])['requests'],1)
if __name__=='__main__':unittest.main(verbosity=2)
