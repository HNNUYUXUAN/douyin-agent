"""Deterministic setup routing; host observations never perform browser actions."""
import json
from pathlib import Path
from browser_state import eligible

ROOT=Path(__file__).resolve().parent.parent

def required_docs(language,host):
    index=json.loads((ROOT/'docs/agent/index.json').read_text(encoding='utf-8'))
    return [p.replace('{host}',host) for p in index['setup_flow']['required_docs'][language]]

def route(local,live,installed,language='zh-CN',host='codex',flow='setup',browser_id=None):
    checks=live.get('checks',{})
    rows=[r for r in live.get('browser_observations',[]) if eligible(r,host) and (not browser_id or r['id']==browser_id)]
    stages=[]
    missing=[k for k in ('python312','ffmpeg','ffprobe','config_present') if not local[k]]
    if missing: stages.append(('local_prerequisites','resolve_local_prerequisites',None,missing))
    if not installed: stages.append(('installation','verify_install_receipt',None,['installed_receipt']))
    if checks.get('skill_discovery',{}).get('status')!='passed':
        stages.append(('discovery','verify_skill_discovery','host_observation',['skill_discovery']))
    if not any(r['capabilities']['screenshot']=='passed' for r in rows):
        stages.append(('browser','verify_user_browser','host_observation',['live_chrome_edge_dom_screenshot']))
    if not local['key_present']: stages.append(('key','wait_for_local_key','local_key',['agent_plan_key_missing']))
    if stages:
        phase,action,waiting,_=stages[0]
        phase_docs={'local_prerequisites':['bootstrap/dependencies.md'],
                    'installation':['operations/install.md'],'discovery':['bootstrap/'+host+'.md','operations/onboarding.md'],
                    'browser':['operations/browser-selection.md'],'key':['bootstrap/key.md']}
        return {'phase':phase,'setup_status':'waiting_for_user' if waiting=='local_key' else 'incomplete',
                'next_action':action,'required_docs':[f'wiki/{language}/'+p for p in phase_docs[phase]],
                'blocking_reasons':[x for s in stages for x in s[3]],'waiting_for':waiting}
    if flow=='acceptance':
        return {'phase':'maintenance','setup_status':'configured_not_service_verified','next_action':'run_explicit_maintenance_acceptance',
                'required_docs':[f'wiki/{language}/bootstrap/clean-test.md',f'wiki/{language}/operations/maintenance.md'],'blocking_reasons':[],'waiting_for':None}
    return {'phase':'complete','setup_status':'configured_not_service_verified',
            'next_action':'finish_setup' if flow=='setup' else 'await_explicit_start',
            'required_docs':[] if flow=='setup' else [f'wiki/{language}/start.md'],'blocking_reasons':[],'waiting_for':None}
