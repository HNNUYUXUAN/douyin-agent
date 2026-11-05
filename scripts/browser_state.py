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
        if set(row)!={'id','family','kind','observed_at','evidence','capabilities','platforms'}: raise ValueError('Invalid browser observation fields')
        identifier(row['id'])
        if row['id'] in seen: raise ValueError('Duplicate browser id')
        seen.add(row['id']); moment(row['observed_at']); evidence(row['evidence'])
        if row['family'] not in ('chrome','edge','other') or row['kind'] not in ('extension','iab','cdp'): raise ValueError('Unsupported browser family/kind')
        c=row['capabilities']
        if not isinstance(c,dict) or set(c)!=CAPABILITIES or any(v not in STATES for v in c.values()): raise ValueError('Record each browser capability separately')
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

def choices(saved):
    result={}; bindings=saved.get('platform_bindings',{})
    for platform in sorted(PLATFORMS):
        rows=[r for r in saved.get('browser_observations',[]) if r['capabilities']['connection']=='passed' and r['capabilities']['dom']=='passed' and platform in r['platforms']]
        preferred=bindings.get(platform,{}).get('browser_id')
        logged=[r for r in rows if r['platforms'][platform]=={'login_state':'logged_in','access':'passed'}]
        candidates=logged or [r for r in rows if r['platforms'][platform]['access']=='passed'] or rows
        selected=next((r for r in candidates if r['id']==preferred),None)
        if selected is None and len(candidates)==1: selected=candidates[0]
        binding=bindings.get(platform,{})
        first=not (selected and selected['id']==preferred and binding.get('first_use_complete'))
        result[platform]={'candidate_ids':[r['id'] for r in candidates],'suggested_browser_id':selected['id'] if selected else None,
                          'action':'reuse_work_tab' if selected and not first else 'first_use_two_tabs' if selected else 'choose_browser' if candidates else 'connect_or_public_link',
                          'requires_live_recheck':True,'historical_only':True}
    return result
