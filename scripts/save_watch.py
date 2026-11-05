"""Observe a known Downloads folder; never reads browser Preferences or user file contents."""
import argparse,ctypes,json,re,uuid
from pathlib import Path
from legacy import read,write,sha,now
from installer import plain

def downloads():
    if __import__('os').name!='nt':raise ValueError('Provide an explicit download directory')
    guid=ctypes.create_string_buffer(uuid.UUID('374DE290-123F-4565-9164-39C4925E467B').bytes_le)
    pointer=ctypes.c_void_p()
    code=ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(guid),0,None,ctypes.byref(pointer))
    if code:raise ValueError('Downloads known folder unavailable; provide explicit directory')
    try:return Path(ctypes.wstring_at(pointer.value))
    finally:ctypes.windll.ole32.CoTaskMemFree(pointer)

def snapshot(directory):
    return {p.name:[p.stat().st_size,p.stat().st_mtime_ns] for p in directory.iterdir() if p.is_file() and not p.is_symlink()}

def before(w,directory=None):
    directory=plain(directory or downloads())
    ident=uuid.uuid4().hex[:12];write(w/'out/save-watch'/f'{ident}.json',{'id':ident,'directory':str(directory),'before':snapshot(directory),'at':now()})
    return {'watch_id':ident,'directory':str(directory),'next_action':'Click the observed parser save control, then inspect once','ownership_claimed':False}

def after(w,ident,expected=None,confirmed=False):
    if not re.fullmatch('[a-f0-9]{12}',ident):raise ValueError('Invalid watch id')
    record=read(w/'out/save-watch'/f'{ident}.json');directory=plain(record['directory']);current=snapshot(directory)
    new=[name for name in current if name not in record['before'] and not name.endswith(('.crdownload','.part','.tmp'))]
    selected=[x for x in new if not expected or x==expected]
    result={'watch_id':ident,'new_candidates':len(new),'ownership_claimed':False}
    if len(selected)!=1:
        return {**result,'status':'ambiguous' if selected else 'not_observed','next_action':'Inspect native save prompt or exact file evidence; do not infer a global host limitation'}
    path=plain(directory/selected[0]);result.update(status='candidate_requires_identity_review',path=str(path),bytes=path.stat().st_size,sha256=sha(path))
    if confirmed:
        if not expected:raise ValueError('Confirm only an exact expected filename and host-verified task creation')
        result.update(status='task_created_confirmed',ownership_claimed=True,owned_downloads=[{'path':str(path),'sha256':sha(path),'created_by_task':True}])
    write(w/'out/save-watch'/f'{ident}-result.json',result);return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',required=True,type=Path)
    sub=p.add_subparsers(dest='action',required=True);q=sub.add_parser('before');q.add_argument('--directory',type=Path)
    q=sub.add_parser('after');q.add_argument('--id',required=True);q.add_argument('--expected-name');q.add_argument('--confirm-created-by-task',action='store_true')
    a=p.parse_args();w=plain(a.workspace)
    result=before(w,a.directory) if a.action=='before' else after(w,a.id,a.expected_name,a.confirm_created_by_task)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
