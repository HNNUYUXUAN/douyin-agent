"""Explicit request recovery; original submissions and reservations are retained."""
import re,uuid
from pathlib import Path
from legacy import read,write,digest,now,sha,within

def events(w):return read(w/'recovery-events.json') if (w/'recovery-events.json').exists() else []
def append(w,event):
    rows=events(w)
    if not any(x.get('event_id')==event['event_id'] for x in rows):write(w/'recovery-events.json',rows+[event])

def rows(w):
    result=[]
    if (w/'requests.json').exists():result=read(w/'requests.json')
    elif (w/'requests.jsonl').exists():
        import json
        result=[json.loads(s) for s in (w/'requests.jsonl').read_text(encoding='utf-8-sig').splitlines() if s.strip()]
    # Pending is the submission intent, written before the ledger and network.
    # Read-only reconstruction preserves a reservation after an interrupted write.
    known={x.get('cache_id') for x in result}
    for p in sorted((w/'cache').glob('*.pending.json')):
        row=read(p)
        if row.get('cache_id') and row['cache_id'] not in known:
            result.append({**row,'recovered_from_pending':True});known.add(row['cache_id'])
    return result
def original(w,key):
    if not re.fullmatch('[a-f0-9]{64}',key):raise ValueError('Use the local 64-character cache_id, not a guessed platform ID')
    row=next((x for x in rows(w) if x['cache_id']==key),None)
    if not row:raise ValueError('Request record not found')
    return row

def authorization(w,key):
    return next((x for x in reversed(events(w)) if x.get('cache_id')==key and x['kind']=='retry_authorized'),None)

def job_name(value):return Path(value or '').name
def abandoned(w,job):return any(x['kind']=='abandon' and job_name(x.get('job'))==job_name(job) for x in events(w))

def blocking(w,row):
    if abandoned(w,row.get('job')):return False
    if row.get('status') not in ('submitted','unresolved'):return False
    key=row.get('cache_id')
    if not key:return True
    if any(x.get('cache_id')==key and x['kind']=='request_abandon' for x in events(w)):return False
    if any(x.get('cache_id')==key and x['kind'] in ('reconciled','retry_completed') for x in events(w)):return False
    # Authorization replaces the effective attempt, not the original accounting reservation.
    if authorization(w,key):return False
    return True

def pending_for_job(w,job):return [r for r in rows(w) if job_name(r.get('job'))==job_name(job) and blocking(w,r)]

def cached_retry(w,key,auth):
    child=next((r for r in rows(w) if r.get('retry_of')==key),None)
    resolved=child and (child['status']=='completed' or any(x.get('cache_id')==child['cache_id'] and x['kind']=='reconciled' for x in events(w)))
    if resolved and (w/'cache'/f"{child['cache_id']}.json").is_file():
        result=read(w/'cache'/f"{child['cache_id']}.json")
        complete_retry(w,key,child['cache_id'],result)
        return result

def complete_retry(w,key,attempt,result):
    write(w/'cache'/f'{key}.json',result)
    append(w,{'event_id':'completed-'+attempt,'kind':'retry_completed','cache_id':key,'attempt_id':attempt,'at':now(),
              'request_id':result.get('id') or result.get('log_id'),'original_terminal_state':'unknown','original_charge_retained':True})

def status(w,key=None):
    selected=rows(w)
    if key:
        original(w,key);selected=[r for r in selected if r['cache_id']==key or r.get('retry_of')==key]
    return {'requests':[{**r,'effective_blocking':blocking(w,r),'cached':(w/'cache'/f"{r['cache_id']}.json").exists()} for r in selected],
            'recovery_events':[x for x in events(w) if not key or x.get('cache_id')==key],
            'billing':'Original reservations retained; returned usage is not settled billing'}

def retry(w,key,approve=None):
    row=original(w,key)
    if (w/'cache'/f'{key}.json').exists():raise ValueError('Complete cache already exists; reconcile and resume')
    if row.get('retry_of') or any(x.get('retry_of')==key for x in rows(w)):
        raise ValueError('One unresolved retry already used; reconcile or abandon')
    if abandoned(w,row['job']) or any(x.get('cache_id')==key and x['kind']=='request_abandon' for x in events(w)):raise ValueError('Work was abandoned; cannot retry')
    if row.get('status') not in ('unresolved','submitted'):raise ValueError('Only an unfinished request may receive a retry preview')
    identity={'cache_id':key,'job':row['job'],'parent_plan':row['plan'],'new_usage':row['charge'],'max_attempts':1}
    plan={**identity,'id':digest(identity)[:24],'created_at':row['at'],'original_charge_retained':True}
    path=w/'out/recovery'/f"{plan['id']}.json"
    if path.exists() and read(path)!=plan:raise ValueError('Recovery preview changed')
    write(path,plan)
    if approve:
        if approve!=plan['id']:raise ValueError('Recovery preview approval mismatch')
        append(w,{'event_id':'authorized-'+key,'kind':'retry_authorized','cache_id':key,'job':row['job'],
                  'retry_plan':plan['id'],'new_usage':row['charge'],'parent_plan':row['plan'],'at':now()})
    action='repeat_original_inspect' if row.get('identity',{}).get('stage')=='ui_vision' else 'resume_original_plan'
    return {**plan,'authorized':bool(authorization(w,key)),'next_action':action if authorization(w,key) else 'authorize_preview_within_existing_user_scope'}

def reconcile(w,key,evidence=None):
    row=original(w,key)
    raw=Path(evidence) if evidence else None
    path=within(w,raw if raw.is_absolute() else w/raw) if raw else w/'cache'/f'{key}.response.json'
    data=read(path) if path.exists() else {}
    trace=data.get('diagnostics',{});response=data.get('response',{})
    saved=w/'cache'/f'{key}.response.json'
    prior=read(saved) if saved.exists() else {}
    known=(prior.get('diagnostics') or {}).get('response_id') or (prior.get('diagnostics') or {}).get('request_id') or row.get('request_id')
    # A process may stop after the complete result is atomically written but before
    # the ledger transition. Require its matching identity and completed trace.
    cached=w/'cache'/f'{key}.json'
    if evidence is None and cached.exists():
        result=read(cached);diagnostics=result.get('diagnostics') or {}
        is_asr=row.get('identity',{}).get('stage')=='asr'
        cache_known=known or diagnostics.get('response_id') or (diagnostics.get('request_id') if is_asr else None)
        complete=(result.get('log_id')==cache_known and isinstance(result.get('data',{}).get('result'),dict)) if is_asr else (result.get('id')==cache_known and bool(result.get('text')))
        if cache_known and complete and diagnostics.get('phase')=='completed':
            append(w,{'event_id':'reconciled-'+key,'kind':'reconciled','cache_id':key,'job':row['job'],'at':now(),
                      'evidence':str(cached.relative_to(w)),'evidence_sha256':sha(cached),'original_charge_retained':True})
            return {'cache_id':key,'reconciled':True,'next_action':'resume_original_plan','original_charge_retained':True}
    text='\n'.join(c.get('text','') for o in response.get('output',[]) for c in o.get('content',[]) if c.get('type')=='output_text')
    if not known or response.get('id')!=known or response.get('status')!='completed' or not text:
        return {'cache_id':key,'reconciled':False,'terminal_state':'unknown_or_unsuccessful','next_action':'retry_preview_or_abandon','original_charge_retained':True}
    result={'id':response['id'],'model':response.get('model'),'text':text,'usage':response.get('usage'),'diagnostics':trace}
    write(w/'cache'/f'{key}.json',result)
    append(w,{'event_id':'reconciled-'+key,'kind':'reconciled','cache_id':key,'job':row['job'],'at':now(),
              'evidence':str(path.relative_to(w)),'evidence_sha256':sha(path),'usage':response.get('usage'),'original_charge_retained':True})
    return {'cache_id':key,'reconciled':True,'next_action':'resume_original_plan','original_charge_retained':True}

def abandon(w,key):
    row=original(w,key)
    if row.get('identity',{}).get('stage')=='ui_vision':
        append(w,{'event_id':'abandon-'+key,'kind':'request_abandon','cache_id':key,'job':row['job'],'at':now(),'original_charge_retained':True})
        write(w/'out/recovery'/f'{key[:24]}-ended.json',{'cache_id':key,'reason':'UI inspection explicitly ended; input screenshot retained','original_terminal_state':'unknown'})
        return None
    append(w,{'event_id':'abandon-'+row['job'],'kind':'abandon','cache_id':key,'job':row['job'],'at':now(),'original_charge_retained':True})
    job=within(w/'out/jobs',w/'out/jobs'/job_name(row['job']))
    write(job/'abandoned.json',{'at':now(),'reason':'Explicitly ended without a completed report','request_ids':[r['cache_id'] for r in rows(w) if r.get('job')==row['job']],
                                'original_terminal_states_retained':True})
    return job
