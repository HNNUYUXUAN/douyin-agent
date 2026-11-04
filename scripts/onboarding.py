"""Local checks and explicit host observations; never calls cloud services."""
import json, os, re, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

CHECKS={'browser_connection','douyin_access','agent_plan_call'}
STATUSES={'passed','blocked','unverified','not_applicable'}
LINKS={
 'browser':'https://learn.chatgpt.com/docs/chrome-extension',
 'workbuddy_browser':'https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar',
 'douyin':'https://www.douyin.com/',
 'agent_plan':'https://www.volcengine.com/activity/agentplan',
 'console':'https://ark.volcengine.com/region:cn-beijing/openManagement?LLM=%7B%7D&advancedActiveKey=agentPlan',
 'guide':'https://docs.volcengine.com/docs/ark/agent-plan-personal-get-started?lang=zh',
 'conda':'https://www.anaconda.com/docs/getting-started/miniconda/install',
 'ffmpeg':'https://ffmpeg.org/download.html'}

def context(w,version):
    return {'schema_version':1,'skill_version':version,'workspace':str(w),'python':sys.executable,
      'skill_root':str(Path(__file__).resolve().parent.parent),'documentation_index':str(Path(__file__).resolve().parent.parent/'docs/agent/index.json'),
      'observations':str(w/'onboarding.json'),'updated_at':datetime.now(timezone.utc).isoformat(),
      'resume_rule':'Read live status, requests.json and pending cache records; historical checks are not current health.'}

def onboard(w,a,version,read,write,config):
    if a.record:
        record=read(Path(a.record))
        if set(record)!={'schema_version','checks'} or record['schema_version']!=1 or not isinstance(record['checks'],dict):
            raise ValueError('Expected schema_version=1 and checks object only')
        if not record['checks'] or set(record['checks'])-CHECKS: raise ValueError('Unknown or empty checks')
        for name,value in record['checks'].items():
            if not isinstance(value,dict) or set(value)!={'status','observed_at','evidence'} or value['status'] not in STATUSES:
                raise ValueError('Each check requires status, observed_at, evidence only')
            stamp=datetime.fromisoformat(value['observed_at'].replace('Z','+00:00'))
            if stamp.tzinfo is None or stamp>datetime.now(timezone.utc): raise ValueError('Use an observed past timezone-aware timestamp')
            evidence=value['evidence']
            if not isinstance(evidence,str) or not evidence or len(evidence)>240: raise ValueError('Provide a short evidence reference')
            if re.search(r'(?i)(bearer|api[_-]?key|token|cookie|afp_|sk-)',evidence): raise ValueError('Evidence must not contain credentials')
            if evidence.startswith('https://'):
                from urllib.parse import urlsplit
                u=urlsplit(evidence)
                if not u.hostname or u.username or u.password or u.query or u.fragment: raise ValueError('Use clean public evidence URLs')
            else:
                p=Path(evidence)
                if p.is_absolute() or p.suffix not in ('.json','.md'): raise ValueError('Use workspace-relative MD/JSON evidence')
                try: resolved=(w/p).resolve(); resolved.relative_to(w)
                except ValueError: raise ValueError('Evidence outside workspace')
                if not resolved.is_file(): raise ValueError('Evidence file missing')
        saved=read(w/'onboarding.json') if (w/'onboarding.json').exists() else {'schema_version':1,'checks':{}}
        saved['checks'].update(record['checks']); write(w/'onboarding.json',saved)
        write(w/'agent-context.json',context(w,version))
    local={'python312':sys.version_info[:2]==(3,12),'config_present':(w/'.env').is_file(),
      'key_present':bool(config(w).get('VOLC_AGENT_API_KEY')),'ffmpeg':bool(shutil.which('ffmpeg')),'ffprobe':bool(shutil.which('ffprobe'))}
    saved=read(w/'onboarding.json') if (w/'onboarding.json').exists() else {'schema_version':1,'checks':{}}
    return {'schema_version':1,'local':local,'historical_host_observations':saved['checks'],
      'cloud_verified_by_this_check':False,'browser_verified_by_this_check':False,'links':LINKS,
      'next_actions':['Resolve missing local prerequisites','Verify selected browser and Douyin access using host tools','Reuse configured Agent Plan; otherwise guide purchase and local key entry','Preview a real task before authorized cloud validation'],
      'record_written':bool(a.record)}
