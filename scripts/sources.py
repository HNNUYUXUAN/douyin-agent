"""Canonical public identities; browser resolution is required for share links."""
import re
from urllib.parse import urlsplit, parse_qs

def online(value, digest):
    match=re.search(r'https?://[^\s<>]+',value)
    if not match: raise ValueError('Expected local media or supported platform URL/share text')
    u=urlsplit(match[0].rstrip('。，,.!')); host=(u.hostname or '').lower()
    if u.username or u.password: raise ValueError('Source credentials are unsupported')
    groups={'douyin':{'douyin.com','www.douyin.com','v.douyin.com','m.douyin.com','www.iesdouyin.com','iesdouyin.com'},
      'youtube':{'youtube.com','www.youtube.com','m.youtube.com','youtu.be'},
      'xiaohongshu':{'xiaohongshu.com','www.xiaohongshu.com','xhslink.com','www.xhslink.com'},
      'tiktok':{'tiktok.com','www.tiktok.com','m.tiktok.com','vm.tiktok.com','vt.tiktok.com'}}
    platform=next((p for p,hosts in groups.items() if host in hosts),None)
    if not platform: raise ValueError('Unsupported source domain')
    ident=None; kind='video'
    if platform=='douyin':
        m=re.search(r'/(video|note)/(\d{15,22})(?:/|$)',u.path)
        if m: kind,ident=m.groups()
        else:
            q=parse_qs(u.query); ident=(q.get('modal_id') or q.get('aweme_id') or [None])[0]
            if ident and not re.fullmatch(r'\d{15,22}',ident): ident=None
        url=f'https://www.douyin.com/{kind}/{ident}'
    elif platform=='youtube':
        ident=u.path.strip('/') if host=='youtu.be' else (parse_qs(u.query).get('v') or [None])[0]
        if not ident:
            m=re.fullmatch(r'/(?:shorts|embed)/([\w-]{11})/?',u.path); ident=m[1] if m else None
        if ident and not re.fullmatch(r'[\w-]{11}',ident): ident=None
        url=f'https://youtu.be/{ident}'
    elif platform=='xiaohongshu':
        m=re.fullmatch(r'/(?:explore|discovery/item)/([a-fA-F0-9]{24})/?',u.path); ident=m[1].lower() if m else None
        kind='note'; url=f'https://www.xiaohongshu.com/explore/{ident}'
    else:
        m=re.fullmatch(r'/@([\w.]+)/video/(\d{15,22})/?',u.path)
        ident=m[2] if m else None; url=f'https://www.tiktok.com/@{m[1]}/video/{ident}' if m else ''
    if not ident: return {'kind':'unresolved','platform':platform,'id':digest(value)[:16],'status':'needs_browser_resolution'}
    return {'kind':kind,'platform':platform,'id':ident,'source_url':url}
