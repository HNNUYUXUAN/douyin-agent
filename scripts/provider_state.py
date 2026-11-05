"""Atomic, replayable provider receipts; parser lookup contains no extraction code."""
import uuid
from pathlib import Path
from legacy import read,write,now

ROUTES=[
 {'platform':'douyin','url':'https://snapany.com/zh/tiktok','types':['video','images'],'evidence':'field v2.5.0/v2.5.1; revalidate current result'},
 {'platform':'bilibili','url':'https://greenvideo.cc/','types':['video'],'evidence':'WorkBuddy v2.5.0 browser save passed; v2.5.1 sample failed'},
 {'platform':'bilibili','url':'https://snapany.com/zh/bilibili','types':['video','images'],'evidence':'video/file 403 differs by sample; image field success'},
 {'platform':'xiaohongshu','url':'https://greenvideo.cc/','types':['video','images'],'evidence':'one image passed; other samples no_result'},
 {'platform':'youtube','url':'https://getfrom.io/en','types':['video'],'evidence':'field saved short video'},
 {'platform':'tiktok','url':'https://snapany.com/zh/tiktok','types':['video','images'],'evidence':'entry observed; TikTok acquisition acceptance pending'}]

def recover(w):
    path=w/'provider-transaction.json'
    if path.exists():
        tx=read(path);write(w/'providers.json',tx['providers']);write(w/'provider-history.json',tx['history']);path.unlink()

def record(w,receipts,apply):
    recover(w)
    rows=read(w/'providers.json') if (w/'providers.json').exists() else []
    history=read(w/'provider-history.json') if (w/'provider-history.json').exists() else []
    results=[]
    for receipt in receipts:
        rows,history,result=apply(rows,history,dict(receipt));results.append(result)
    # Validation completed before the durable intent. Replay completes either interrupted write.
    write(w/'provider-transaction.json',{'schema_version':1,'providers':rows,'history':history})
    recover(w)
    return results

def overview(w,platform=None,round_id=None):
    root=Path(__file__).resolve().parent.parent
    history=read(w/'provider-history.json') if (w/'provider-history.json').exists() else []
    selected=[x for x in history if not round_id or x.get('round_id')==round_id]
    latest={(x['url'],x['host'],x.get('round_id')):x for x in selected}
    from urllib.parse import urlsplit
    sites={urlsplit(x['url']).hostname.lower().removeprefix('www.') for x in selected}
    return {'routes':[{**x,'needs_live_validation':True} for x in ROUTES if not platform or x['platform']==platform],
            'round_id':round_id,'remaining_sources':max(0,3-len(sites)) if round_id else None,
            'unclosed_attempts':[x for x in latest.values() if x['outcome']=='attempting'],
            'sample_index':str(root/'docs/agent/samples.json'),'transaction_recovery_required':(w/'provider-transaction.json').exists()}
