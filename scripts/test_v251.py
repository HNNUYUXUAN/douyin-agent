import copy,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from datetime import datetime,timezone,timedelta
from types import SimpleNamespace as A
from unittest.mock import patch
import browser_state as bs,setup_flow as sf,onboarding,knowledge,da

class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.w=Path(self.tmp.name).resolve()
  self.stamp=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat()
 def tearDown(self):self.tmp.cleanup()
 def row(self,i='chrome',kind='extension',login='logged_in',caps=True):
  return {'id':i,'kind':kind,'family':i if i in ('chrome','edge') else 'other','observed_at':self.stamp,'evidence':'proof.md',
          'capabilities':dict.fromkeys(bs.CAPABILITIES,'passed'),'host_capabilities':['user_tabs'] if caps else [],
          'platforms':{'bilibili':{'login_state':login,'access':'passed'}}}
 def live(self):
  return {'schema_version':2,'checks':{'skill_discovery':{'status':'passed','observed_at':self.stamp,'evidence':'proof.md'}},'browser_observations':[self.row()]}
 def test_iab_is_never_platform_candidate(self):
  r=self.row('iab','iab');r['platforms']['bilibili']['login_state']='logged_in'
  result=bs.choices({'browser_observations':[r]})['bilibili']
  self.assertEqual(result['candidate_ids'],[]);self.assertEqual(result['action'],'connect_user_browser')
 def test_explicit_missing_browser_never_falls_back(self):
  result=bs.choices({'browser_observations':[self.row('edge'),self.row('iab','iab')]},browser_id='chrome')['bilibili']
  self.assertIsNone(result['suggested_browser_id']);self.assertEqual(result['requested_browser_id'],'chrome')
  blocked=self.row();blocked['platforms']['bilibili']['access']='blocked'
  result=bs.choices({'browser_observations':[blocked,self.row('edge')]},browser_id='chrome')['bilibili']
  self.assertEqual(result['suggested_browser_id'],'chrome');self.assertEqual(result['action'],'platform_blocked')
 def test_workbuddy_requires_observed_user_tabs_legacy_is_readable(self):
  old=self.row(caps=False);old.pop('host_capabilities')
  bs.validate({'browser_observations':[old]},lambda x:None)
  self.assertEqual(bs.choices({'browser_observations':[old]},'workbuddy')['bilibili']['candidate_ids'],[])
  self.assertEqual(bs.choices(self.live(),'workbuddy')['bilibili']['suggested_browser_id'],'chrome')
 def test_login_tab_is_conditional_even_on_reused_work_tab(self):
  saved=self.live();saved['platform_bindings']={'bilibili':{'browser_id':'chrome','first_use_complete':True,'work_tab':'w','login_tab':'a'}}
  result=bs.choices(saved)['bilibili']
  self.assertEqual(result['action'],'reuse_work_tab');self.assertEqual(result['login_action'],'not_needed')
  self.assertEqual(result['login_tab_to_release_if_task_owned'],'a')
  for state in ('unknown','logged_out'):
   saved['browser_observations'][0]['platforms']['bilibili']['login_state']=state
   self.assertEqual(bs.choices(saved)['bilibili']['login_action'],'reserve_login_tab')
 def test_binding_before_other_logged_in_and_explicit_override(self):
  saved={'browser_observations':[self.row('chrome',login='logged_out'),self.row('edge')],
         'platform_bindings':{'bilibili':{'browser_id':'chrome','first_use_complete':True}}}
  self.assertEqual(bs.choices(saved)['bilibili']['suggested_browser_id'],'chrome')
  self.assertEqual(bs.choices(saved,browser_id='edge')['bilibili']['suggested_browser_id'],'edge')
 def test_missing_platform_requires_probe(self):
  self.assertEqual(bs.choices(self.live())['douyin']['action'],'probe_platform')
 def test_key_gate_and_setup_stops_without_paid_sample(self):
  local=dict.fromkeys(('python312','ffmpeg','ffprobe','config_present','key_present'),True);local['key_present']=False
  r=sf.route(local,self.live(),True,host='workbuddy')
  self.assertEqual(r['next_action'],'wait_for_local_key');self.assertEqual(r['waiting_for'],'local_key')
  self.assertEqual(r['required_docs'],['wiki/zh-CN/bootstrap/key.md'])
  local['key_present']=True
  r=sf.route(local,self.live(),True,host='workbuddy')
  self.assertEqual(r['next_action'],'finish_setup');self.assertEqual(r['required_docs'],[])
  self.assertEqual(sf.route(local,self.live(),True,flow='use')['next_action'],'await_explicit_start')
  self.assertEqual(sf.route(local,self.live(),True,flow='acceptance')['next_action'],'run_explicit_maintenance_acceptance')
 def test_saved_observations_cannot_complete_new_setup_check(self):
  local=dict.fromkeys(('python312','ffmpeg','ffprobe','config_present','key_present'),True)
  r=sf.route(local,{},True)
  self.assertEqual(r['phase'],'discovery');self.assertIn('live_chrome_edge_dom_screenshot',r['blocking_reasons'])
 def test_check_observed_does_not_write_progress_or_leak_key(self):
  (self.w/'proof.md').write_text('public observation');da.write(self.w/'current.json',self.live())
  (self.w/'.env').write_text('VOLC_AGENT_API_KEY=private-fixture')
  before={p.name:p.read_bytes() for p in self.w.iterdir()}
  r=onboarding.onboard(self.w,A(record=None,observed=self.w/'current.json',host='workbuddy'),'2.5.1',da.read,lambda *x:self.fail('read-only check wrote'),lambda w:{'VOLC_AGENT_API_KEY':'private-fixture'})
  self.assertNotIn('private-fixture',json.dumps(r));self.assertEqual(before,{p.name:p.read_bytes() for p in self.w.iterdir()})
  self.assertFalse(r['cloud_verified_by_this_check']);self.assertEqual(len(r['next_actions']),1)
 def test_all_fault_ids_route_to_existing_body_in_both_languages(self):
  index=json.loads((sf.ROOT/'docs/agent/index.json').read_text(encoding='utf-8'))
  rows=index['setup_flow']['fault_routes'];self.assertEqual(sum(x['code'].split('-')[0] in ('F24','F241','I','O') for x in rows),42)
  for row in rows:
   for lang in ('zh-CN','en'):
    target=knowledge.route(row['code'],lang)['required_docs'][0]
    self.assertTrue((sf.ROOT/target).is_file(),target)
  self.assertFalse(knowledge.route('not-a-known-fault','zh-CN')['matched'])
 def test_required_pack_language_host_and_no_acceptance(self):
  for lang in ('zh-CN','en'):
   for host in ('workbuddy','codex'):
    docs=sf.required_docs(lang,host)
    self.assertEqual(len(docs),6)
    for p in docs:self.assertTrue((sf.ROOT/p).is_file());self.assertNotIn('clean-test',p)
  self.assertLessEqual((sf.ROOT/'SKILL.md').stat().st_size,2048)
 def test_no_result_counts_site_and_is_not_parser_success(self):
  p=self.w/'provider.json'
  def record(site,outcome='no_result',rnd='work-one'):
   da.write(p,{'url':'https://'+site+'/parser','host':'fixture','search_source':'https://search.example','outcome':outcome,'round_id':rnd})
   return da.provider(self.w,A(receipt=p))
  record('first.example')
  self.assertFalse(da.provider(self.w,A(receipt=None))['providers'][0]['previously_verified'])
  record('second.example');record('third.example')
  with self.assertRaisesRegex(ValueError,'Three provider'):record('fourth.example')
  record('fourth.example',rnd='different-work')
 def test_record_progress_and_v1_merge(self):
  (self.w/'proof.md').write_text('public');p=self.w/'r.json';da.write(p,self.live())
  onboarding.onboard(self.w,A(record=p,host='workbuddy'),'2.5.1',da.read,da.write,lambda w:{})
  progress=da.read(self.w/'setup-progress.json')
  self.assertEqual(progress['evidence'],['proof.md']);self.assertNotIn('key',progress)
  da.write(p,{'schema_version':1,'checks':{'browser_connection':{'status':'passed','observed_at':self.stamp,'evidence':'proof.md'}}})
  r=onboarding.onboard(self.w,A(record=p,host='workbuddy'),'2.5.1',da.read,da.write,lambda w:{})
  self.assertEqual(r['browser_choices']['bilibili']['suggested_browser_id'],'chrome')
  self.assertNotEqual(r['phase'],'complete')

if __name__=='__main__':unittest.main(verbosity=2)
