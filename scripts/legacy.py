"""Host-triggered Agent Plan evidence pipeline. No automatic paid retries."""


from __future__ import annotations


import argparse, asyncio, base64, gzip, hashlib, json, math, os, re, shutil, struct, subprocess, sys, time, uuid


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
    for k in ('VOLC_AGENT_API_KEY','VOLC_AGENT_MODEL','VOLC_AGENT_REASONING','VOLC_AGENT_CONNECT_TIMEOUT','VOLC_AGENT_READ_TIMEOUT','BOCHA_API_KEY','TENCENTCLOUD_WSA_APIKEY'):
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
    result={'duration':float(d.get('format',{}).get('duration',0)), 'has_audio':any(s['codec_type']=='audio' for s in d['streams']), 'has_video':any(s['codec_type']=='video' for s in d['streams'])}
    video=next((s for s in d['streams'] if s['codec_type']=='video'),{})
    try:
        start=float(video.get('start_time',0))-float(d.get('format',{}).get('start_time',0)); duration=float(video['duration'])
        if math.isfinite(start+duration) and duration>0: result['video_end']=start+duration
    except (KeyError,ValueError,TypeError): pass
    return result


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
    from cloud_transport import Trace,SETTINGS
    trace=Trace('asr');trace.data['phase']='decoding_audio';trace.begin()
    task=None;upload_start=None;upload_end=None
    try:
        pcm=command(['ffmpeg','-v','error','-i',p,'-ar','16000','-ac','1','-f','s16le','-'])
        headers={'X-Api-Key':key,'X-Api-Resource-Id':'volc.seedasr.sauc.duration','X-Api-Connect-Id':str(uuid.uuid4())}
        trace.data['phase']='connecting'
        async with websockets.connect(ASR,additional_headers=headers,open_timeout=SETTINGS['connect_timeout'],max_size=16*1024*1024) as ws:
            trace.data.update(request_id=ws.response.headers.get('X-Tt-Logid'),response_headers_seconds=trace.elapsed(),phase='uploading_audio')
            payload={'user':{'uid':'douyin-agent'},'audio':{'format':'pcm','codec':'raw','rate':16000,'bits':16,'channel':1},'request':{'model_name':'bigmodel','enable_itn':True,'enable_punc':True,'show_utterances':True,'result_type':'full'}}
            await ws.send(packet(1,1,json.dumps(payload).encode()))
            async def receive():
                while True:
                    d,final=parse_packet(await ws.recv())
                    if trace.data['first_event_seconds'] is None:trace.data['first_event_seconds']=trace.elapsed()
                    if d.get('code',0) not in (0,1000,20000000):raise RuntimeError('ASR service code '+str(d['code']))
                    if final:return {'data':d,'log_id':ws.response.headers.get('X-Tt-Logid')}
            task=asyncio.create_task(receive());upload_start=time.monotonic()
            for i,pos in enumerate(range(0,len(pcm),6400)):
                await ws.send(packet(2,i+2,pcm[pos:pos+6400],pos+6400>=len(pcm)))
                await asyncio.sleep(.2)
            upload_end=time.monotonic();trace.data['phase']='waiting_recognition'
            result=await asyncio.wait_for(task,SETTINGS['read_timeout'])
            trace.data.update(phase='completed',completed_seconds=trace.elapsed(),upload_seconds=upload_end-upload_start,recognition_wait_seconds=time.monotonic()-upload_end)
            trace.finish();result['diagnostics']=trace.data;return result
    except BaseException as exc:
        trace.data.update(error_type=type(exc).__name__,upload_seconds=(upload_end or time.monotonic())-upload_start if upload_start else None,
                          recognition_wait_seconds=time.monotonic()-upload_end if upload_end else None)
        trace.finish();exc.response_data={'diagnostics':trace.data,'status':'transport_interrupted'};raise
    finally:
        trace.stop.set()
        if task and not task.done():
            task.cancel()
            try:await task
            except asyncio.CancelledError:pass


def response(key,model,content,options=None):
    from cloud_transport import response as call
    return call(API,key,model,content,options)


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
