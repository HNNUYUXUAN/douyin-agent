import copy,json,os,shutil,subprocess,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace as A
from unittest.mock import patch
from datetime import datetime,timezone,timedelta
import da,browsing,legacy,onboarding,browser_state,knowledge
from PIL import Image

class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.w=Path(self.tmp.name).resolve()
  self.c={'platforms':['bilibili','youtube'],'mode':'all','entry':'public links','selection':'','max_seconds':600,'max_items':2,'image_dwell_seconds':3,'limits':{'requests':4,'images':10,'audio_seconds':10,'search_requests':2}}
 def tearDown(self): self.tmp.cleanup()
 def test_bilibili_identity_and_parts(self):
  a=legacy.source('https://www.bilibili.com/video/BV1dC4y117Rz/?p=2&share_source=secret')
  self.assertEqual(a['id'],'BV1dC4y117Rz-p2');self.assertNotIn('secret',json.dumps(a))
  self.assertEqual(legacy.source('https://www.bilibili.com/video/BV1dC4y117Rz')['part'],1)
  self.assertEqual(legacy.source('https://www.bilibili.com/opus/1234')['id'],legacy.source('https://t.bilibili.com/1234')['id'])
  for url in ('https://b23.tv/abc','https://www.bilibili.com/video/av1234','https://www.douyin.com/shipin/1234567890123456789'):
   self.assertEqual(legacy.source(url)['kind'],'unresolved')
  with self.assertRaises(ValueError):legacy.source('https://bilibili.com.evil.org/video/BV1dC4y117Rz')
  with self.assertRaises(ValueError):legacy.source('https://www.bilibili.com/video/BV1dC4y117Rz/?p=0')
 def test_authorization_is_session_bound_and_legacy_reads(self):
  a=browsing.create(self.w,self.c);b=browsing.create(self.w,self.c)
  self.assertNotEqual(a['approval_id'],b['approval_id'])
  with self.assertRaises(ValueError):browsing.change(self.w,b['id'],'approve',a['approval_id'])
  a.pop('schema_version');a['approval_id']=legacy.digest(a['config'])[:24];legacy.write(browsing.root(self.w,a['id'])/'session.json',a)
  self.assertEqual(browsing.load(self.w,a['id'])[1]['approval_id'],a['approval_id'])
 def test_cross_platform_identity_isolation(self):
  self.c['platforms']=['douyin','tiktok'];s=browsing.create(self.w,self.c);browsing.change(self.w,s['id'],'approve',s['approval_id'])
  ident='7581709508896984366'
  a=browsing.record(self.w,s['id'],{'source':f'https://www.douyin.com/video/{ident}','status':'observed'})
  b=browsing.record(self.w,s['id'],{'source':f'https://www.tiktok.com/@example/video/{ident}','status':'observed'})
  self.assertNotEqual(a['identity'],b['identity'])
 def test_platform_block_does_not_create_work_or_spend_item_cap(self):
  s=browsing.create(self.w,self.c);browsing.change(self.w,s['id'],'approve',s['approval_id'])
  row=browsing.record(self.w,s['id'],{'source':'https://www.bilibili.com/','status':'deferred','reason':'login_required'})
  self.assertNotIn('identity',row)
  for part in (1,2):browsing.record(self.w,s['id'],{'source':f'https://www.bilibili.com/video/BV1dC4y117Rz/?p={part}','status':'observed'})
  state=browsing.load(self.w,s['id'])[1];self.assertEqual(len(state['items']),2);self.assertEqual(len(state['pending']),1)
  with self.assertRaises(ValueError):browsing.scope_job(self.w,s['id'],{'source':legacy.source('https://www.bilibili.com/opus/1234')},[])
 def media(self):
  p=self.w/'original.png';Image.new('RGB',(40,40)).save(p);return p
 def test_parser_route_requires_recorded_source_and_preserves_user_import(self):
  p=self.media();receipt=self.w/'receipt.json';url='https://www.bilibili.com/opus/1234'
  r={'identity_verified':True,'expected_images':1,'order_verified':True,'route':'parser','provider':'https://example.org/parser','host':'fixture','round_id':'work-1234'}
  legacy.write(receipt,r)
  with self.assertRaisesRegex(ValueError,'recorded provider'):da.adopt(self.w,A(source=url,media=[p],receipt=receipt,title='',author=''))
  provider=self.w/'provider.json';legacy.write(provider,{'url':r['provider'],'host':'fixture','search_source':'https://example.org','instructions':'public parser','types':['images'],'outcome':'attempting','round_id':r['round_id']})
  da.provider(self.w,A(receipt=provider));result=da.adopt(self.w,A(source=url,media=[p],receipt=receipt,title='',author=''))
  self.assertEqual(result['integrity']['status'],'passed')
  r['route']='user_import';r['owned_downloads']=[{'path':str(p),'sha256':da.sha(p),'created_by_task':True}];legacy.write(receipt,r)
  with self.assertRaisesRegex(ValueError,'preserved'):da.adopt(self.w,A(source=url,media=[p],receipt=receipt,title='',author=''))
 def test_native_provider_history_is_not_a_parser_recommendation(self):
  r={'url':'https://api.bilibili.com/','host':'fixture','search_source':'https://example.org','outcome':'attempting','round_id':'work'}
  p=self.w/'provider.json';legacy.write(p,r)
  with self.assertRaisesRegex(ValueError,'third-party parser'):da.provider(self.w,A(receipt=p))
  legacy.write(self.w/'providers.json',[{**r,'outcome':'success','last_success':'2026-01-01T00:00:00Z'}])
  old=da.provider(self.w,A(receipt=None))['providers'][0]
  self.assertFalse(old['previously_verified']);self.assertTrue(old['needs_live_validation'])
 def test_source_round_counts_sites_across_browsers(self):
  p=self.w/'provider.json'
  for site in ('a.example','b.example','c.example'):
   legacy.write(p,{'url':'https://'+site+'/first','host':'chrome','search_source':'https://search.example','outcome':'login_required','round_id':'same-work'})
   da.provider(self.w,A(receipt=p))
  legacy.write(p,{'url':'https://www.a.example/another-path','host':'edge','search_source':'https://search.example','outcome':'attempting','round_id':'same-work'})
  da.provider(self.w,A(receipt=p))
  r=legacy.read(p);r['url']='https://fourth.example/';legacy.write(p,r)
  with self.assertRaisesRegex(ValueError,'Three provider sources'):da.provider(self.w,A(receipt=p))
 def test_windows_slash_cleanup_keeps_hash_and_ownership_guards(self):
  p=self.media();j=self.w/'out/jobs/cleanup';j.mkdir(parents=True)
  legacy.write(j/'ownership.json',[{'path':str(p),'sha256':da.sha(p),'kind':'browser_download'}])
  legacy.write(j/'acquisition.json',{'owned_downloads':[{'path':str(p).replace('\\','/'),'sha256':da.sha(p),'created_by_task':True}]})
  self.assertEqual(da.clean_owned(self.w,j),[]);self.assertFalse(p.exists())
 def test_imported_zip_preserves_original_and_cleans_extracted_copies(self):
  import zipfile,unpack_images
  original=self.media();archive=self.w/'user-original.zip'
  with zipfile.ZipFile(archive,'w') as z:z.write(original,'1.png')
  output=self.w/'out/acquire/imported';manifest=unpack_images.unpack(archive,self.w,output,1)
  image=Path(manifest['images'][0]['path']);receipt=self.w/'import.json'
  r={'route':'user_import','identity_verified':True,'expected_images':1,'order_verified':True,'import_manifest':'out/acquire/imported/manifest.json','owned_artifacts':[{'path':str(image),'sha256':da.sha(image),'created_by_task':True}]}
  legacy.write(receipt,r);result=da.adopt(self.w,A(source='https://www.bilibili.com/opus/1234',media=[image],receipt=receipt,title='',author=''))
  j=Path(result['job']);self.assertEqual(result['integrity']['status'],'passed')
  self.assertEqual(da.clean_owned(self.w,j),[]);self.assertTrue(archive.exists());self.assertTrue(original.exists());self.assertFalse(image.exists());self.assertTrue((output/'manifest.json').exists())
  legacy.write(self.w/'provider.json',{'url':'https://example.org/parser','search_source':'https://example.org','host':'fixture','outcome':'success','job':str(j)})
  with self.assertRaisesRegex(ValueError,'must match'):da.provider(self.w,A(receipt=self.w/'provider.json'))
 def observation(self):
  stamp=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat()
  def row(i,f,p):return {'id':i,'family':f,'kind':'extension','observed_at':stamp,'evidence':'proof.json','capabilities':dict.fromkeys(browser_state.CAPABILITIES,'passed'),'platforms':p}
  return {'schema_version':2,'checks':{},'browser_observations':[row('chrome','chrome',{'bilibili':{'login_state':'logged_in','access':'passed'},'youtube':{'login_state':'logged_out','access':'passed'}}),row('edge','edge',{'youtube':{'login_state':'logged_in','access':'passed'}})]}
 def test_cross_browser_selection_first_tabs_and_v1_merge(self):
  legacy.write(self.w/'proof.json',{});r=self.observation();record=self.w/'record.json';legacy.write(record,r)
  result=onboarding.onboard(self.w,A(record=record),'2.5.0',legacy.read,legacy.write,lambda w:{})
  self.assertEqual(result['browser_choices']['youtube']['suggested_browser_id'],'edge')
  self.assertEqual(result['browser_choices']['bilibili']['action'],'open_work_tab')
  self.assertEqual(result['browser_choices']['bilibili']['login_action'],'not_needed')
  r['platform_bindings']={'bilibili':{'browser_id':'chrome','work_tab':'20','login_tab':'19','first_use_complete':True,'observed_at':r['browser_observations'][0]['observed_at'],'evidence':'proof.json'}}
  legacy.write(record,r);result=onboarding.onboard(self.w,A(record=record),'2.5.0',legacy.read,legacy.write,lambda w:{})
  self.assertEqual(result['browser_choices']['bilibili']['action'],'reuse_work_tab')
  legacy.write(record,{'schema_version':1,'checks':{'bilibili_access':{'status':'passed','observed_at':r['browser_observations'][0]['observed_at'],'evidence':'proof.json'}}})
  result=onboarding.onboard(self.w,A(record=record),'2.5.0',legacy.read,legacy.write,lambda w:{})
  self.assertEqual(result['browser_choices']['youtube']['suggested_browser_id'],'edge')
 def test_browser_ambiguity_failure_and_screenshot_independence(self):
  r=self.observation();r['browser_observations'][1]['platforms']['bilibili']={'login_state':'logged_in','access':'passed'}
  self.assertEqual(browser_state.choices(r)['bilibili']['action'],'choose_browser')
  r['browser_observations'][0]['capabilities']['connection']='blocked'
  self.assertEqual(browser_state.choices(r)['bilibili']['suggested_browser_id'],'edge')
  r['browser_observations'][1]['capabilities']['screenshot']='blocked'
  self.assertEqual(browser_state.choices(r)['bilibili']['suggested_browser_id'],'edge')
  r['browser_observations'][1]['id']='private profile name'
  with self.assertRaises(ValueError):browser_state.validate(r,lambda x:None)
 def test_actual_mismatched_stream_sampling(self):
  if not shutil.which('ffmpeg'):self.skipTest('FFmpeg unavailable')
  p=self.w/'unequal.mp4'
  subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','testsrc=size=64x64:rate=10:duration=0.7','-f','lavfi','-i','sine=duration=1','-c:v','mpeg4','-c:a','aac','-y',str(p)],check=True,capture_output=True)
  r=da.adopt(self.w,A(source=str(p),media=[p],receipt=None,title='',author=''));j=Path(r['job']);rows=da.sample(j)
  self.assertGreater(len(rows),0);self.assertLessEqual(max(x['time'] for x in rows),.7);self.assertTrue(p.exists())
  self.assertEqual(da.read(j/'metadata.json')['input_hashes'],[da.sha(p)])
  with patch.object(da,'probe',return_value={'video_end':1.0}):
   da.sample(j)
  self.assertTrue(any(x['reason']=='tail_frame_skipped' for x in da.read(j/'sampling.json')['notes']))
  original=da.core.command
  def fail_middle(args):
   if '-ss' in args and args[args.index('-ss')+1]=='0.5':raise subprocess.CalledProcessError(1,args)
   return original(args)
  with patch.object(da.core,'command',side_effect=fail_middle):
   with self.assertRaises(subprocess.CalledProcessError):da.sample(j)
 def test_mixed_search_reaches_operational_body(self):
  self.assertTrue(knowledge.search([('public',knowledge.BUNDLE)],'download parser 解析站'))

if __name__=='__main__':unittest.main(verbosity=2)
