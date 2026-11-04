"""Host-triggered Agent Plan evidence pipeline. No automatic paid retries."""


from __future__ import annotations


import argparse, asyncio, base64, gzip, hashlib, json, os, re, shutil, struct, subprocess, sys, time, uuid


from pathlib import Path


from datetime import datetime, timezone


import requests


from dotenv import dotenv_values


from PIL import Image, ImageDraw


VERSION='1.0.0'


API='https://ark.cn-beijing.volces.com/api/plan/v3/responses'


ASR='wss://openspeech.bytedance.com/api/v3/plan/sauc/bigmodel_nostream'


MODEL='doubao-seed-2.1-pro'


ACCEPTANCE=False


REQUEST_LIMIT=10


ACTIVE_JOB=None


def now(): return datetime.now(timezone.utc).isoformat()


def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def write(p,x):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_suffix(p.suffix+'.tmp'); t.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8'); t.replace(p)


def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()


def command(args): return subprocess.check_output([str(x) for x in args],stderr=subprocess.PIPE)


def config(w):
    c=dict(dotenv_values(w/'.env',encoding='utf-8-sig'))
    for k in ('VOLC_AGENT_API_KEY','VOLC_AGENT_MODEL','VOLC_AGENT_REASONING','BOCHA_API_KEY','TENCENTCLOUD_WSA_APIKEY'):
        if k in os.environ: c[k]=os.environ[k]
    return c


def within(w,p):
    p=Path(p).resolve(); p.relative_to(w.resolve())
    if len(str(p))>160: raise ValueError('Path exceeds 160 characters')
    return p


def source(s):
    if '://' not in s and len(s)<260 and Path(s).is_file(): return {'kind':'local','id':sha(s)[:16]}
    from sources import online
    return online(s,digest)


def probe(p):
    d=json.loads(command(['ffprobe','-v','error','-show_format','-show_streams','-of','json',p]))
    return {'duration':float(d.get('format',{}).get('duration',0)), 'has_audio':any(s['codec_type']=='audio' for s in d['streams']), 'has_video':any(s['codec_type']=='video' for s in d['streams'])}


def packet(kind,seq,payload,final=False):
    b=gzip.compress(payload); flags=3 if final else 1
    return bytes([0x11,(kind<<4)|flags,0x11 if kind==1 else 0x01,0])+struct.pack('>iI',-seq if final else seq,len(b))+b


def parse_packet(b):
    if isinstance(b,str): raise ValueError('Unexpected text ASR response')
    offset=(b[0]&15)*4; kind=b[1]>>4; flags=b[1]&15
    if kind==15:
        code=struct.unpack_from('>I',b,offset)[0]; raise RuntimeError('ASR service code '+str(code))
    if flags&1: offset+=4
    size=struct.unpack_from('>I',b,offset)[0]; payload=b[offset+4:offset+4+size]
    if b[2]&15==1: payload=gzip.decompress(payload)
    return json.loads(payload),bool(flags&2)


async def recognize(p,key):
    import websockets
    pcm=command(['ffmpeg','-v','error','-i',p,'-ar','16000','-ac','1','-f','s16le','-'])
    headers={'X-Api-Key':key,'X-Api-Resource-Id':'volc.seedasr.sauc.duration','X-Api-Connect-Id':str(uuid.uuid4())}
    async with websockets.connect(ASR,additional_headers=headers,open_timeout=30,max_size=16*1024*1024) as ws:
        payload={'user':{'uid':'douyin-agent'},'audio':{'format':'pcm','codec':'raw','rate':16000,'bits':16,'channel':1},'request':{'model_name':'bigmodel','enable_itn':True,'enable_punc':True,'show_utterances':True,'result_type':'full'}}
        await ws.send(packet(1,1,json.dumps(payload).encode()))
        async def receive():
            while True:
                d,final=parse_packet(await ws.recv())
                if d.get('code',0) not in (0,1000,20000000): raise RuntimeError('ASR service code '+str(d['code']))
                if final: return {'data':d,'log_id':ws.response.headers.get('X-Tt-Logid')}
        task=asyncio.create_task(receive())
        try:
            for i,pos in enumerate(range(0,len(pcm),6400)):
                await ws.send(packet(2,i+2,pcm[pos:pos+6400],pos+6400>=len(pcm)))
                await asyncio.sleep(.2)
            return await asyncio.wait_for(task,90)
        finally:
            if not task.done(): task.cancel()


def response(key,model,content,options=None):
    # requests defaults to zero retries; redirect following disabled with credentials.
    payload={'model':model,'input':[{'role':'user','content':content}],'max_output_tokens':16384,'store':False,'stream':True}
    if options: payload.update(options)
    r=requests.post(API,headers={'Authorization':'Bearer '+key},json=payload,stream=True,timeout=(30,90),allow_redirects=False)
    if r.status_code!=200: raise RuntimeError('Responses HTTP '+str(r.status_code))
    d={}; partial=''
    try:
        for line in r.iter_lines():
            if not line.startswith(b'data:'): continue
            payload=line[5:].strip()
            if payload==b'[DONE]': break
            event=json.loads(payload)
            if event.get('type')=='response.output_text.delta': partial+=event.get('delta','')
            if isinstance(event.get('response'),dict): d=event['response']
            if event.get('type') in ('response.completed','response.incomplete','response.failed'): break
    except Exception as e:
        e.response_data={'response':d,'partial_text':partial,'status':'transport_interrupted'}; raise
    finally: r.close()
    text='\n'.join(c.get('text','') for o in d.get('output',[]) for c in o.get('content',[]) if c.get('type')=='output_text')
    if not text or d.get('status') not in (None,'completed'):
        e=RuntimeError('Incomplete Responses result'); e.response_data=d; raise e
    return {'id':d.get('id'),'model':d.get('model'),'text':text,'usage':d.get('usage')}


def search(w,job,query,submit=None):
    c=config(w); rows=[]; failures=[]
    for provider,var,url,body in [('yuanbao','TENCENTCLOUD_WSA_APIKEY','https://api.wsa.cloud.tencent.com/SearchPro',{'Query':query,'Cnt':10}),('bocha','BOCHA_API_KEY','https://api.bocha.cn/v1/web-search',{'query':query,'count':10,'summary':True,'freshness':'noLimit'})]:
        if not c.get(var): continue
        try:
            def request():
                r=requests.post(url,headers={'Authorization':'Bearer '+c[var]},json=body,timeout=40,allow_redirects=False)
                return {'http':r.status_code,'data':r.json() if r.status_code==200 else {}}
            result=submit(provider,body,request) if submit else request()
            if result['http']!=200: failures.append({'provider':provider,'http':result['http']}); continue
            d=result['data']
            if provider=='yuanbao':
                for page in d.get('Response',{}).get('Pages',[]):
                    x=json.loads(page); rows.append({'title':x.get('title'),'url':x.get('url'),'summary':x.get('passage'),'site':x.get('site')})
            else:
                rows=[{'title':x.get('name'),'url':x.get('url'),'summary':x.get('summary') or x.get('snippet'),'site':x.get('siteName')} for x in d.get('data',{}).get('webPages',{}).get('value',[])]
            if rows: break
        except requests.RequestException: failures.append({'provider':provider,'status':'transport_error'})
    record={'query':query,'at':now(),'sources':rows,'failures':failures,'status':'retrieved_not_verified' if rows else 'unavailable'}
    write(job/'research.json',record)
    text='# 外部核查来源 / External verification sources\n\n检索结果不是对作品内容的证明。逐项阅读原始来源后再形成核查结论。\n\n'
    for i,row in enumerate(rows): text+=f"[{i+1}] [{row['title']}]({row['url']}) — {row['site']}\n\n{row['summary']}\n\n"
    (job/'research.md').write_text(text,encoding='utf-8'); return record
