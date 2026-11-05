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
      'xiaohongshu':{'xiaohongshu.com','www.xiaohongshu.com','xhslink.com','www.xhslink.com','xhslink.cn','www.xhslink.cn'},
      'tiktok':{'tiktok.com','www.tiktok.com','m.tiktok.com','vm.tiktok.com','vt.tiktok.com'},
      'bilibili':{'bilibili.com','www.bilibili.com','m.bilibili.com','t.bilibili.com','b23.tv'}}
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
    elif platform=='bilibili':
        video=re.fullmatch(r'/video/(BV[0-9A-Za-z]{10})/?',u.path)
        dynamic=re.fullmatch(r'/opus/([0-9]{1,22})/?',u.path)
        if host=='t.bilibili.com': dynamic=re.fullmatch(r'/([0-9]{1,22})/?',u.path)
        if host!='b23.tv' and video:
            parts=parse_qs(u.query).get('p',['1'])
            if len(parts)!=1 or not re.fullmatch(r'[1-9][0-9]{0,5}',parts[0]): raise ValueError('Invalid Bilibili part')
            part=int(parts[0]); bv=video[1]; ident=f'{bv}-p{part}'
            return {'kind':'video','platform':platform,'id':ident,'bvid':bv,'part':part,
                    'source_url':f'https://www.bilibili.com/video/{bv}/?p={part}'}
        if host!='b23.tv' and dynamic:
            ident='dynamic-'+dynamic[1]; kind='note'; url=f'https://www.bilibili.com/opus/{dynamic[1]}'
    else:
        m=re.fullmatch(r'/@([\w.]+)/video/(\d{15,22})/?',u.path)
        ident=m[2] if m else None; url=f'https://www.tiktok.com/@{m[1]}/video/{ident}' if m else ''
    if not ident:
        return {'kind':'unresolved','platform':platform,'id':digest(value)[:16],'status':'needs_browser_resolution',
                'entry_url':'https://'+host+u.path,
                'reason':'noncanonical_shipin_route' if platform=='douyin' and u.path.startswith('/shipin/') else 'resolve_visible_work_page'}
    return {'kind':kind,'platform':platform,'id':ident,'source_url':url}
