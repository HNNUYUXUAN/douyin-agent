"""Local checks and explicit host observations; never calls cloud services."""
import json, os, re, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

CHECKS={'skill_discovery','browser_connection','douyin_access','youtube_access','xiaohongshu_access','tiktok_access','bilibili_access','visual_inspection','agent_plan_call','search_available','file_save'}
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

def evidence_reference(w,evidence):
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

def onboard(w,a,version,read,write,config):
    if getattr(a,'browser_id',None):
        from browser_state import identifier
        identifier(a.browser_id)
    observed=getattr(a,'observed',None)
    if a.record and observed: raise ValueError('Use --record or --observed, not both')
    live={}
    if a.record or observed:
        record=read(Path(a.record or observed))
        v=record.get('schema_version')
        allowed={'schema_version','checks'} if v==1 else {'schema_version','checks','browser_observations','platform_bindings'}
        if v not in (1,2) or set(record)-allowed or not isinstance(record.get('checks'),dict):
            raise ValueError('Expected schema_version 1/2 and checks; v2 permits browser_observations/platform_bindings')
        if set(record['checks'])-CHECKS or not (record['checks'] or (v==2 and (record.get('browser_observations') or record.get('platform_bindings')))): raise ValueError('Unknown or empty checks')
        for name,value in record['checks'].items():
            if not isinstance(value,dict) or set(value)!={'status','observed_at','evidence'} or value['status'] not in STATUSES:
                raise ValueError('Each check requires status, observed_at, evidence only')
            stamp=datetime.fromisoformat(value['observed_at'].replace('Z','+00:00'))
            if stamp.tzinfo is None or stamp>datetime.now(timezone.utc): raise ValueError('Use actual system UTC time with timezone, at or before the current system clock')
            evidence_reference(w,value['evidence'])
        if v==2:
            from browser_state import validate
            validate(record,lambda e:evidence_reference(w,e))
        live=record
    saved=read(w/'onboarding.json') if (w/'onboarding.json').exists() else {'schema_version':1,'checks':{}}
    if a.record:
        record=live
        if record['schema_version']==2:
            merged={r['id']:r for r in saved.get('browser_observations',[])}
            merged.update({r['id']:r for r in record.get('browser_observations',[])})
            saved['browser_observations']=list(merged.values())
            saved.setdefault('platform_bindings',{}).update(record.get('platform_bindings',{}))
            for platform,binding in saved['platform_bindings'].items():
                if binding['browser_id'] not in merged or platform not in merged[binding['browser_id']]['platforms']:
                    raise ValueError('Binding requires a recorded browser/platform observation')
            saved['schema_version']=2
        saved['checks'].update(record['checks']); write(w/'onboarding.json',saved)
        write(w/'agent-context.json',context(w,version))
    local={'python312':sys.version_info[:2]==(3,12),'config_present':(w/'.env').is_file(),
      'key_present':bool(config(w).get('VOLC_AGENT_API_KEY')),'ffmpeg':bool(shutil.which('ffmpeg')),'ffprobe':bool(shutil.which('ffprobe')),
      'curl':bool(shutil.which('curl.exe') or shutil.which('curl'))}
    ws=read(w/'workspace.json') if (w/'workspace.json').exists() else {}
    skill=Path(ws.get('skill_root',str(Path(__file__).resolve().parent.parent)))
    host=getattr(a,'host',None) or ('workbuddy' if {'.workbuddy','.codebuddy'} & set(skill.parts) else 'codex')
    installed=False
    if (skill/'installed.json').is_file():
        receipt=read(skill/'installed.json')
        installed=bool(receipt.get('workspace')) and Path(receipt['workspace']).resolve()==w and receipt.get('version')==version
    from browser_state import choices
    from setup_flow import route
    flow=getattr(a,'flow','setup'); language=getattr(a,'language','zh-CN'); browser_id=getattr(a,'browser_id',None)
    routing=route(local,live,installed,language,host,flow,browser_id)
    if a.record:
        write(w/'setup-progress.json',{'schema_version':1,'flow':flow,'phase':routing['phase'],
            'next_action':routing['next_action'],'waiting_for':routing['waiting_for'],
            'evidence':sorted({x['evidence'] for x in live.get('checks',{}).values()}|{x['evidence'] for x in live.get('browser_observations',[])}),
            'updated_at':datetime.now(timezone.utc).isoformat()})
    return {'schema_version':2,'flow':flow,'host':host,'local':local,'historical_host_observations':saved['checks'],
      'browser_choices':choices(live if observed else saved,host,browser_id),**routing,
      'local_config_path':str(w/'.env'),'live_observations_supplied':bool(live),
      'cloud_verified_by_this_check':False,'browser_verified_by_this_check':False,'links':LINKS,
      'next_actions':[routing['next_action']],
      'record_written':bool(a.record)}
