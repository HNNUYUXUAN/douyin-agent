"""Read/search OKF knowledge and explicitly store sanitized local cases (stdlib only)."""
import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

BUNDLE = Path(__file__).resolve().parent.parent / 'wiki'
SPEC = 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md'


def stamp():
    return datetime.now(timezone.utc).isoformat()


def plain(path):
    p = Path(os.path.abspath(path))
    if len(str(p)) > 160:
        raise ValueError('Knowledge path exceeds 160 characters; choose a shorter workspace or case id')
    for item in (p, *p.parents):
        if item.is_symlink() or (item.exists() and getattr(item.lstat(), 'st_file_attributes', 0) & 0x400):
            raise ValueError('Linked knowledge paths are unsupported')
    return p


def atomic(path, text):
    plain(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex[:8] + '.tmp')
    try:
        temp.write_text(text, encoding='utf-8', newline='\n')
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def document(path):
    text = path.read_text(encoding='utf-8')
    if path.name in ('index.md', 'log.md'):
        return None, text
    match = re.match(r'\A---\n(.*?)\n---\n(.*)\Z', text, re.S)
    if not match:
        raise ValueError('Missing frontmatter: ' + path.name)
    # JSON mappings are valid YAML. This writer/reader deliberately uses that subset.
    data = json.loads(match[1])
    if not isinstance(data, dict) or not isinstance(data.get('type'), str) or not data['type'].strip():
        raise ValueError('Missing nonempty type: ' + path.name)
    return data, match[2]


def concepts(root):
    if not root.exists():
        return []
    plain(root)
    rows = []
    for p in sorted(root.rglob('*.md')):
        plain(p)
        meta, body = document(p)
        if meta:
            rows.append((p, meta, body))
    return rows


def reindex(root):
    rows = concepts(root)
    entries = ['# Local cases / 本地问题记录', '']
    log = ['# Local knowledge log', '']
    groups = {}
    for p, meta, body in rows:
        rel = p.relative_to(root).as_posix()
        entries.append(f"- [{meta['title']}]({rel}) - {meta['description']}")
        day = meta['generated']['at'][:10]
        groups.setdefault(day, []).append(f"- **Record**: [{meta['title']}]({rel})")
    for day in sorted(groups, reverse=True):
        log += ['## ' + day, *groups[day], '']
    atomic(root / 'index.md', '\n'.join(entries) + '\n')
    atomic(root / 'log.md', '\n'.join(log) + '\n')
    return {'cases': len(rows), 'index': str(root / 'index.md')}


def safe_text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 4000:
        raise ValueError('Use nonempty short text fields (maximum 4000 characters)')
    if re.search(r'(?i)(bearer\s|api[_-]?key\s*[:=]|cookie\s*[:=]|\bsk-[A-Za-z0-9]|data:(image|video|audio)/|[A-Z]:[\\/]|https?://[^\s]+[?#])', value):
        raise ValueError('Remove credentials, private paths, media encodings and signed/query URLs')
    return value.strip()


def record(workspace, source):
    data = json.loads(Path(source).read_text(encoding='utf-8-sig'))
    required = {'id', 'title', 'symptom', 'action', 'result', 'verification', 'keywords', 'sources'}
    if set(data) != required or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,47}', data['id']):
        raise ValueError('Use the documented fields and a short ASCII case id')
    for key in required - {'id', 'keywords', 'sources'}:
        data[key] = safe_text(data[key])
    if not isinstance(data['keywords'], list) or not data['keywords'] or len(data['keywords']) > 20:
        raise ValueError('Provide 1-20 keywords')
    tags = [safe_text(x) for x in data['keywords']]
    if not isinstance(data['sources'], list) or not data['sources']:
        raise ValueError('At least one evidence source is required')
    sources = []
    for item in data['sources']:
        safe_text(item)
        if item.startswith('workspace:'): item=item[len('workspace:'):]
        u = urlsplit(item)
        if u.scheme:
            if u.scheme != 'https' or not u.hostname or u.username or u.password or u.query or u.fragment:
                raise ValueError('Use clean public HTTPS URL or existing workspace-relative MD/JSON evidence')
        else:
            evidence = plain(workspace / item)
            evidence.relative_to(workspace)
            if evidence.suffix not in ('.json', '.md') or not evidence.is_file():
                raise ValueError('Use existing workspace-relative MD/JSON evidence')
            item = 'workspace:' + Path(item).as_posix()
        sources.append({'resource': item})
    root = plain(workspace / 'knowledge-private')
    target = plain(root / 'cases' / (data['id'] + '.md'))
    if '\n' in data['title'] or any(c in data['title'] for c in '[]()') or len(data['title']) > 120:
        raise ValueError('Use a short single-line title without Markdown link syntax')
    if '\n' in data['symptom'] or len(data['symptom']) > 240:
        raise ValueError('Use a single-line symptom of at most 240 characters')
    if target.exists():
        raise ValueError('Case already exists; use a new revision id and link the prior case')
    meta = {'type': 'Troubleshooting Case', 'title': data['title'], 'description': data['symptom'],
            'tags': tags, 'status': 'draft', 'generated': {'by': 'process:douyin-agent-knowledge', 'at': stamp()},
            'sources': sources}
    body = '\n\n'.join('# ' + label + '\n\n' + data[key] for label, key in
                           [('Symptom', 'symptom'), ('Action', 'action'), ('Result', 'result'), ('Verification', 'verification')])
    # Exclusive publication; index/log can be rebuilt after interruption with reindex.
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8', newline='\n') as f:
        f.write('---\n' + json.dumps(meta, ensure_ascii=False, indent=2) + '\n---\n\n' + body + '\n')
    return {'case': str(target), **reindex(root)}


def search(roots, query):
    terms = query.casefold().split()
    rows = []
    for label, root in roots:
        for p, meta, body in concepts(root):
            text = (json.dumps(meta, ensure_ascii=False) + '\n' + body).casefold()
            score = sum(term in text for term in terms)
            if score:
                rows.append({'scope': label, 'path': str(p), 'title': meta.get('title', p.stem),
                             'status': meta.get('status', 'unspecified'), 'score': score})
    return sorted(rows, key=lambda r: (-r['score'], r['path']))[:20]

def validate_bundle(root):
    rows=concepts(root)
    for path,meta,body in rows:
        if path.stat().st_size>8192: raise ValueError('Split oversized OKF concept: '+path.name)
        for source in meta.get('sources',[]):
            if not isinstance(source,dict) or not isinstance(source.get('resource'),str) or not source['resource'].strip():
                raise ValueError('Invalid OKF source: '+path.name)
        for name in ('generated','verified'):
            entry=meta.get(name)
            if isinstance(entry,dict) and entry.get('at'):
                stamp=datetime.fromisoformat(entry['at'].replace('Z','+00:00'))
                if stamp.tzinfo is None: raise ValueError('OKF timestamps need an explicit timezone')
    for path in root.rglob('*.md') if root.exists() else []:
        for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if ref.startswith(('https://','http://','#','mailto:')): continue
            target=(path.parent/ref.split('#',1)[0]).resolve()
            if not target.is_file(): raise ValueError('Broken OKF link: '+path.name+' -> '+ref)
    return len(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', type=Path, required=True)
    sub = p.add_subparsers(dest='command', required=True)
    for name in ('init', 'reindex', 'validate'):
        sub.add_parser(name)
    sub.add_parser('search').add_argument('--query', required=True)
    sub.add_parser('record').add_argument('--file', type=Path, required=True)
    a = p.parse_args(); w = plain(a.workspace)
    if a.command in ('init', 'reindex'):
        out = reindex(plain(w / 'knowledge-private'))
    elif a.command == 'record':
        out = record(w, a.file)
    elif a.command == 'search':
        out = search([('public', BUNDLE), ('private', w / 'knowledge-private')], a.query)
    else:
        out = {'profile': 'OKF 0.2 JSON-compatible YAML frontmatter',
               'public_concepts': validate_bundle(BUNDLE), 'private_concepts': validate_bundle(w / 'knowledge-private')}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'blocked', 'error': str(error)}, ensure_ascii=False))
        sys.exit(1)
