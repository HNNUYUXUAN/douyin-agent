"""Agent Plan transport diagnostics. No HTTP retries or response storage upstream."""
import json, math, re, threading, time
from datetime import datetime, timezone
import requests

SETTINGS={'connect_timeout':30.0,'read_timeout':300.0}

def configure(values):
    for field,key in [('connect_timeout','VOLC_AGENT_CONNECT_TIMEOUT'),('read_timeout','VOLC_AGENT_READ_TIMEOUT')]:
        value=float(values.get(key) or (30 if field=='connect_timeout' else 300))
        if not math.isfinite(value) or not 1<=value<=1800: raise ValueError(key+' must be between 1 and 1800 seconds')
        SETTINGS[field]=value

def safe_error(value):
    text=str(value)[:2000]
    text=re.sub(r'(?i)(bearer\s+|(?:api[_-]?key|authorization|cookie)\s*[:=]\s*)\S+',r'\1[redacted]',text)
    return re.sub(r'https?://[^\s"<>]+','[url]',text)

class CloudError(RuntimeError):
    def __init__(self,category,data):
        super().__init__('Agent Plan '+category+'; inspect request diagnostics')
        self.category=category;self.response_data=data

class Trace:
    def __init__(self,stage):
        self.start=time.monotonic();self.stop=threading.Event()
        self.data={'stage':stage,'phase':'starting','submitted_at':datetime.now(timezone.utc).isoformat(),
                   'response_id':None,'request_id':None,'model':None,'http_status':None,'usage':None,
                   'response_headers_seconds':None,'first_event_seconds':None,'first_text_seconds':None,'completed_seconds':None}
    def elapsed(self):return round(time.monotonic()-self.start,6)
    def begin(self):
        def heartbeat():
            while not self.stop.wait(15):
                print(json.dumps({'event':'request_progress','stage':self.data['stage'],'phase':self.data['phase'],'elapsed_seconds':self.elapsed()}),flush=True)
        threading.Thread(target=heartbeat,daemon=True).start()
    def finish(self):
        self.stop.set();self.data['elapsed_seconds']=self.elapsed();self.data['ended_at']=datetime.now(timezone.utc).isoformat()

def events(lines):
    data=[]
    for line in lines:
        if isinstance(line,bytes):line=line.decode('utf-8')
        if not line:
            if data:yield '\n'.join(data);data=[]
        elif line.startswith('data:'):
            # Most providers use one JSON data line. Accept both that form and multiline SSE.
            if data:
                try:json.loads('\n'.join(data))
                except ValueError:pass
                else:yield '\n'.join(data);data=[]
            data.append(line[5:].lstrip())
    if data:yield '\n'.join(data)

def response(api,key,model,content,options=None):
    payload={'model':model,'input':[{'role':'user','content':content}],'max_output_tokens':8192,'store':False,'stream':True}
    if options:payload.update(options)
    payload['store']=False;payload['stream']=True
    trace=Trace('responses');trace.data.update(phase='waiting_response_headers',requested_model=model,**SETTINGS);trace.begin()
    r=None;d={};partial='';terminal=None
    try:
        r=requests.post(api,headers={'Authorization':'Bearer '+key},json=payload,stream=True,
                        timeout=(SETTINGS['connect_timeout'],SETTINGS['read_timeout']),allow_redirects=False)
        trace.data.update(http_status=r.status_code,response_headers_seconds=trace.elapsed(),
                          request_id=r.headers.get('X-Request-Id') or r.headers.get('X-Tt-Logid'),phase='http_response')
        if r.status_code!=200:
            try:error=r.json().get('error',{})
            except (ValueError,AttributeError):error={}
            trace.data['error']={k:safe_error(str(error[k]).replace(key,'[redacted]')) for k in ('code','type','message') if k in error}
            category='authentication' if r.status_code in (401,403) else 'quota' if r.status_code==429 else 'configuration' if r.status_code in (400,404,422) else 'http_error'
            raise CloudError(category,{'diagnostics':trace.data})
        trace.data['phase']='reading_events'
        for raw in events(r.iter_lines(chunk_size=1)):
            if raw=='[DONE]':break
            event=json.loads(raw)
            if trace.data['first_event_seconds'] is None:trace.data['first_event_seconds']=trace.elapsed()
            if event.get('type')=='response.output_text.delta':
                partial+=event.get('delta','')
                if trace.data['first_text_seconds'] is None:trace.data['first_text_seconds']=trace.elapsed()
            if isinstance(event.get('response'),dict):
                d=event['response']
                for target,source in (('response_id','id'),('model','model'),('usage','usage')):
                    if d.get(source) is not None:trace.data[target]=d[source]
            if event.get('type') in ('response.completed','response.incomplete','response.failed'):
                terminal=event['type'];break
        trace.data.update(phase='validating_terminal',terminal_event=terminal)
        text='\n'.join(c.get('text','') for o in d.get('output',[]) for c in o.get('content',[]) if c.get('type')=='output_text')
        if terminal!='response.completed' or d.get('status','completed')!='completed' or not text:
            raise CloudError('incomplete_output',{'diagnostics':trace.data,'response':d,'partial_text':partial})
        trace.data.update(phase='completed',completed_seconds=trace.elapsed());trace.finish()
        return {'id':d.get('id'),'model':d.get('model'),'text':text,'usage':d.get('usage'),'diagnostics':trace.data}
    except BaseException as exc:
        trace.data.update(error_type=type(exc).__name__);trace.finish()
        if isinstance(exc,CloudError):
            exc.response_data.update(diagnostics=trace.data);raise
        exc.response_data={'diagnostics':trace.data,'response':d,'partial_text':partial,'status':'transport_interrupted'}
        raise
    finally:
        trace.stop.set()
        if r is not None:r.close()
