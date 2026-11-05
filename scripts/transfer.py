"""Bounded curl transport and owned-file receipts; no platform stream extraction."""
import argparse,concurrent.futures,hashlib,json,math,os,re,shutil,subprocess,time,uuid
from pathlib import Path
from urllib.parse import urlsplit
from legacy import read,write,sha,now,within
from installer import plain

def headers(path):
    text=path.read_text(encoding='iso-8859-1')
    blocks=re.split(r'(?m)^HTTP/\S+ ',text)
    block=blocks[-1];result={}
    for line in block.splitlines()[1:]:
        if ':' in line:
            k,v=line.split(':',1);result[k.lower().strip()]=v.strip()
    return result

def curl(url,out,header,byte_range=None,validator=None,timeout=300):
    exe=shutil.which('curl.exe') or shutil.which('curl')
    if not exe:raise ValueError('Existing curl is unavailable; use host saving or user import')
    args=[exe,'--disable','--silent','--show-error','--location','--proto','=https','--proto-redir','=https',
          '--max-redirs','5','--connect-timeout','30','--max-time',str(timeout),'--speed-limit','65536','--speed-time','30',
          '--output',str(out),'--dump-header',str(header),'--write-out','%{http_code}','--config','-']
    if byte_range:args+=['--range',f'{byte_range[0]}-{byte_range[1]}']
    if validator:args+=['--header','If-Range: '+validator]
    # The ephemeral signed file URL stays out of process arguments and diagnostic logs.
    result=subprocess.run(args,input='url = '+json.dumps(url)+'\n',text=True,capture_output=True,timeout=timeout+15)
    return result.returncode,int(result.stdout[-3:]) if result.stdout[-3:].isdigit() else 0

def ranged(url,directory,expected_sha,count=8,call=curl):
    if not 1<=count<=8:raise ValueError('Range count must be 1..8')
    probe=directory/'probe.part';head=directory/'probe.headers'
    code,status=call(url,probe,head,(0,0))
    h=headers(head) if head.exists() else {};match=re.fullmatch(r'bytes 0-0/(\d+)',h.get('content-range',''))
    if code or status!=206 or not match or probe.stat().st_size!=1:raise ValueError('Origin did not prove byte Range support')
    total=int(match[1])
    if total<1:raise ValueError('Invalid Range resource size')
    validator=h.get('etag');validator_key='etag'
    if validator and validator.startswith('W/'):validator=None
    if not validator:validator=h.get('last-modified');validator_key='last-modified'
    if not validator:raise ValueError('Range origin needs a stable ETag or Last-Modified')
    count=min(count,total);size=math.ceil(total/count);intervals=[(a,min(total-1,a+size-1)) for a in range(0,total,size)]
    def segment(i):
        start,end=intervals[i];out=directory/f'p{i:02}.part';hp=directory/f'p{i:02}.headers'
        for attempt in range(2):
            rc,sc=call(url,out,hp,(start,end),validator)
            if rc==0:break
            if attempt or rc not in (7,18,28,35,52,56):raise ValueError('Range segment transport failed')
        fields=headers(hp)
        if sc!=206 or fields.get('content-range')!=f'bytes {start}-{end}/{total}' or out.stat().st_size!=end-start+1:
            raise ValueError('Range interval or segment length mismatch')
        if fields.get(validator_key)!=validator:raise ValueError('Origin changed during segmented download')
        return out
    with concurrent.futures.ThreadPoolExecutor(max_workers=count) as pool:parts=list(pool.map(segment,range(len(intervals))))
    merged=directory/'merged.part'
    with merged.open('xb') as stream:
        for part in parts:
            with part.open('rb') as src:shutil.copyfileobj(src,stream)
    if merged.stat().st_size!=total or sha(merged)!=expected_sha:raise ValueError('Merged artifact SHA256 mismatch')
    return merged

def media_check(path,kind):
    if kind=='image':
        from PIL import Image
        with Image.open(path) as im:
            width,height=im.size;im.verify()
        return {'kind':'image','width':width,'height':height}
    from legacy import probe
    info=probe(path)
    if not info.get('has_video') or info['duration']<=0:raise ValueError('Saved object is not a playable video')
    proc=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'],capture_output=True)
    if proc.returncode:raise ValueError('Saved video failed full decode')
    return info

def cleanup(w,ident):
    if not re.fullmatch('[a-f0-9]{12}',ident):raise ValueError('Invalid transfer id')
    record=read(w/'out/transfers'/f'{ident}.json');errors=[]
    for row in record['owned_artifacts']:
        p=plain(w/row['path']);p.relative_to(w)
        if not p.exists():continue
        if not p.is_file() or sha(p)!=row['sha256']:errors.append({'path':row['path'],'reason':'changed; retained'});continue
        p.unlink()
    record['cleanup_errors']=errors;record['cleanup_at']=now();write(w/'out/transfers'/f'{ident}.json',record)
    return record

def download(w,url,output,dependency=False,expected_sha=None,provider_receipt=None,kind='video',ranges=8,call=curl):
    u=urlsplit(url)
    if u.scheme!='https' or not u.hostname or u.username or u.password or '\n' in url or '\r' in url:raise ValueError('Use an actual public HTTPS file URL without credentials')
    if dependency:
        allowed=u.hostname in ('repo.anaconda.com','gyan.dev','www.gyan.dev') or (u.hostname=='github.com' and u.path.startswith('/BtbN/FFmpeg-Builds/releases/'))
        if not allowed or not expected_sha or not re.fullmatch('[a-fA-F0-9]{64}',expected_sha):raise ValueError('Dependency needs official-listed origin and expected SHA256')
    else:
        if not provider_receipt:raise ValueError('Parser result needs its recorded source receipt')
        receipt=read(provider_receipt)
        history=read(w/'provider-history.json') if (w/'provider-history.json').exists() else []
        if not any(x['url']==receipt.get('url') and x['host']==receipt.get('host') and x.get('round_id')==receipt.get('round_id') for x in history):
            raise ValueError('Record the parser attempt before saving its visible file result')
    raw=Path(output)
    if raw.is_absolute():raise ValueError('Output must be a new workspace-relative path')
    target=plain(w/raw);target.relative_to(w)
    if target.exists():raise ValueError('Output already exists; preserve it')
    ident=uuid.uuid4().hex[:12];directory=plain(w/'out/transfers'/ident);directory.mkdir(parents=True)
    record={'id':ident,'at':now(),'state':'transferring','dependency':dependency,'file_url_sha256':hashlib.sha256(url.encode()).hexdigest(),
            'output':str(target.relative_to(w)),'owned_artifacts':[],'route':'dependency' if dependency else 'parser','headers_policy':'no_custom_ua_referer_cookie'}
    receipt_path=w/'out/transfers'/f'{ident}.json';write(receipt_path,record)
    try:
        temp=directory/'whole.part';hp=directory/'whole.headers';rc,status=call(url,temp,hp)
        record['http_status']=status
        if rc or status!=200:
            if dependency and (rc in (18,28,35,52,56) or status==206):temp=ranged(url,directory,expected_sha.lower(),ranges,call)
            else:raise ValueError('Transfer failed; inspect HTTP status, keep same parser round')
        if expected_sha and sha(temp)!=expected_sha.lower():raise ValueError('Artifact SHA256 mismatch')
        record['integrity']= {'sha256_verified':True} if dependency else media_check(temp,kind)
        target.parent.mkdir(parents=True,exist_ok=True)
        # Publish the verified file atomically and exclusively on the same volume.
        # A failed copy must never leave an unregistered partial .mp4.
        os.link(temp,target);temp.unlink()
        record.update(state='saved',sha256=sha(target),bytes=target.stat().st_size)
        record['owned_artifacts'].append({'path':str(target.relative_to(w)),'sha256':sha(target),'created_by_task':True})
        return record
    except BaseException as exc:
        record.update(state='failed',error_type=type(exc).__name__)
        raise
    finally:
        for p in directory.iterdir():
            if p.is_file():
                # Do not retain redirect headers containing temporary signed URLs.
                if p.suffix=='.headers':p.unlink()
                else:
                    item={'path':str(p.relative_to(w)),'sha256':sha(p),'created_by_task':True}
                    if record['state']=='saved':p.unlink();item['retired']=True
                    record['owned_artifacts'].append(item)
        write(receipt_path,record)
        if not dependency and record['state']=='failed':
            from da import provider
            from types import SimpleNamespace
            terminal={k:receipt[k] for k in ('url','host','round_id')};terminal.update(search_source=receipt.get('search_source',receipt['url']),outcome='parsed_download_failed')
            p=directory/'source-result.json';write(p,terminal)
            provider(w,SimpleNamespace(receipt=p))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',required=True,type=Path)
    sub=p.add_subparsers(dest='action',required=True)
    d=sub.add_parser('save');u=d.add_mutually_exclusive_group(required=True);u.add_argument('--url');u.add_argument('--url-stdin',action='store_true');d.add_argument('--output',required=True);d.add_argument('--dependency',action='store_true');d.add_argument('--sha256');d.add_argument('--provider-receipt');d.add_argument('--kind',choices=['video','image'],default='video');d.add_argument('--ranges',type=int,default=8)
    d=sub.add_parser('cleanup');d.add_argument('--id',required=True)
    a=p.parse_args();w=plain(a.workspace)
    from media_tools import configure
    configure(w)
    if a.action=='save' and a.url_stdin:
        import sys
        a.url=sys.stdin.read(12000).strip()
    result=cleanup(w,a.id) if a.action=='cleanup' else download(w,a.url,a.output,a.dependency,a.sha256,a.provider_receipt,a.kind,a.ranges)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,subprocess.SubprocessError):
        print(json.dumps({'status':'blocked','next_action':'inspect_transfer_receipt; preserve original parser round'}));raise SystemExit(1)
