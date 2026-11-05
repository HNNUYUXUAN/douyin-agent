"""Validate host observations and suggest browser reuse; never reads profiles/cookies."""
from datetime import datetime, timezone
from browsing import PLATFORMS

CAPABILITIES={'connection','dom','screenshot','file_save'}
STATES={'passed','blocked','unverified'}

def moment(value):
    t=datetime.fromisoformat(value.replace('Z','+00:00'))
    if t.tzinfo is None or t>datetime.now(timezone.utc): raise ValueError('Use actual observation time with timezone')

def identifier(value):
    import re
    if not isinstance(value,str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,100}',value):
        raise ValueError('Use an opaque browser/tab id, without account or profile names')

def validate(record, evidence):
    browsers=record.get('browser_observations',[])
    if not isinstance(browsers,list): raise ValueError('browser_observations must be a list')
    seen=set()
    for row in browsers:
        if set(row)-{'id','family','kind','observed_at','evidence','capabilities','platforms','host_capabilities'} or not {'id','family','kind','observed_at','evidence','capabilities','platforms'}<=set(row): raise ValueError('Invalid browser observation fields')
        identifier(row['id'])
        if row['id'] in seen: raise ValueError('Duplicate browser id')
        seen.add(row['id']); moment(row['observed_at']); evidence(row['evidence'])
        if row['family'] not in ('chrome','edge','other') or row['kind'] not in ('extension','iab','cdp'): raise ValueError('Unsupported browser family/kind')
        c=row['capabilities']
        if not isinstance(c,dict) or set(c)!=CAPABILITIES or any(v not in STATES for v in c.values()): raise ValueError('Record each browser capability separately')
        if 'host_capabilities' in row and (not isinstance(row['host_capabilities'],list) or any(x not in {'navigation','screenshot','cua','batch','dom_cua','user_tabs','visibility','download'} for x in row['host_capabilities'])):
            raise ValueError('Use observed host capability names only')
        if not isinstance(row['platforms'],dict) or set(row['platforms'])-PLATFORMS: raise ValueError('Unknown browser platform')
        for p in row['platforms'].values():
            if set(p)!={'login_state','access'} or p['login_state'] not in ('logged_in','logged_out','unknown') or p['access'] not in STATES:
                raise ValueError('Record login and page access independently')
    bindings=record.get('platform_bindings',{})
    if not isinstance(bindings,dict) or set(bindings)-PLATFORMS: raise ValueError('Unknown binding platform')
    for platform,row in bindings.items():
        if set(row)!={'browser_id','login_tab','work_tab','first_use_complete','observed_at','evidence'}: raise ValueError('Invalid platform binding fields')
        for key in ('browser_id','work_tab'): identifier(row[key])
        if row['login_tab'] is not None: identifier(row['login_tab'])
        if type(row['first_use_complete']) is not bool: raise ValueError('first_use_complete must be boolean')
        moment(row['observed_at']); evidence(row['evidence'])

def eligible(row,host='codex'):
    """Platform pages require a user browser; IAB remains an auxiliary tool only."""
    return (row.get('family') in ('chrome','edge') and row.get('kind')=='extension'
            and row.get('capabilities',{}).get('connection')=='passed'
            and row.get('capabilities',{}).get('dom')=='passed'
            and (host!='workbuddy' or 'user_tabs' in row.get('host_capabilities',[])))

def choices(saved,host='codex',browser_id=None):
    result={}; bindings=saved.get('platform_bindings',{})
    for platform in sorted(PLATFORMS):
        connected=[r for r in saved.get('browser_observations',[]) if eligible(r,host)]
        rows=[r for r in connected if r.get('platforms',{}).get(platform,{}).get('access')!='blocked'] or connected
        preferred=bindings.get(platform,{}).get('browser_id')
        logged=[r for r in rows if r.get('platforms',{}).get(platform)=={'login_state':'logged_in','access':'passed'}]
        if browser_id:
            identifier(browser_id)
            candidates=[r for r in connected if r['id']==browser_id]
            selected=candidates[0] if candidates else None
        else:
            selected=next((r for r in rows if r['id']==preferred and r.get('platforms',{}).get(platform,{}).get('access')=='passed'),None)
            candidates=([selected] if selected else logged or [r for r in rows if r.get('platforms',{}).get(platform,{}).get('access')=='passed'] or rows)
            if selected is None and len(candidates)==1: selected=candidates[0]
        binding=bindings.get(platform,{})
        observed=selected.get('platforms',{}).get(platform,{}) if selected else {}
        reuse=selected and selected['id']==preferred and binding.get('first_use_complete')
        action=('platform_blocked' if selected and observed.get('access')=='blocked' else
                'probe_platform' if selected and observed.get('access')!='passed' else
                'reuse_work_tab' if reuse else 'open_work_tab' if selected else
                'connect_user_browser' if browser_id or not candidates else 'choose_browser')
        result[platform]={'candidate_ids':[r['id'] for r in candidates],'suggested_browser_id':selected['id'] if selected else None,
                          'action':action,'requested_browser_id':browser_id,
                          'login_action':'not_needed' if selected and observed.get('login_state')=='logged_in' else 'reserve_login_tab' if selected else 'wait_for_browser',
                          'login_tab_to_release_if_task_owned':binding.get('login_tab') if selected and observed.get('login_state')=='logged_in' else None,
                          'requires_live_recheck':True,'historical_only':True}
    return result
