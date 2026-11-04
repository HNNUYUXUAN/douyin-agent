"""Windows installation transactions shared by PowerShell and Git Bash (stdlib only)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import uuid
from datetime import datetime, timezone

SOURCE = Path(__file__).resolve().parent.parent
CONDA_GUIDE = 'https://www.anaconda.com/docs/getting-started/miniconda/install'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain(path):
    """Inspect lexical ancestors before resolving any Windows reparse point."""
    p = Path(os.path.abspath(path))
    for item in (p, *p.parents):
        if os.path.lexists(item):
            info = item.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('Linked path unsupported: ' + str(item))
    return p


def relative(name):
    if (not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_.\-/]+', name)
            or Path(name).is_absolute() or any(x in ('', '.', '..') for x in name.replace('\\', '/').split('/'))):
        raise ValueError('Unsafe manifest path')
    return name


def within(path, root):
    return path == root or root in path.parents


def atomic(path, value):
    plain(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex[:8] + '.tmp')
    try:
        with tmp.open('x', encoding='utf-8', newline='\n') as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write('\n')
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def run(argv):
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    subprocess.run([str(x) for x in argv], env=env, check=True)


def default_workspace():
    return Path('D:/douyin-agent') if Path('D:/').is_dir() else Path.home() / 'douyin-agent'


def workspace_path(value):
    if not value:
        suggested = default_workspace()
        value = input('Workspace [' + str(suggested) + ']: ').strip() or str(suggested)
    w = plain(value)
    if len(str(w)) > 85:
        raise ValueError('Choose a shorter workspace path (85 characters maximum)')
    # Existing ancestors may contain user names/spaces; newly created components stay ASCII.
    for item in (w, *w.parents):
        if not item.exists() and not re.fullmatch(r'[A-Za-z0-9_. -]+', item.name):
            raise ValueError('New workspace names must use short ASCII names')
    return w


def prepare(w, conda, source=SOURCE, record=True):
    plain(w)
    for name in ('out', 'cache', 'envs', 'qa'):
        plain(w / name).mkdir(parents=True, exist_ok=True)
    py = plain(w / 'envs/runtime/python.exe')
    if not py.exists():
        run([conda, 'create', '-y', '--override-channels', '-c', 'conda-forge', '--prefix', py.parent,
             '--file', source / 'conda-win-64.lock'])
    run([py, '-B', '-c', "import sys; assert sys.version_info[:2]==(3,12), 'Expected Python 3.12'"])
    run([py, '-B', '-m', 'pip', 'install', '-r', source / 'requirements.lock'])
    env = plain(w / '.env')
    if not env.exists():
        # Exclusive creation preserves configuration created concurrently by the user.
        with env.open('xb') as f:
            f.write((source / 'env.template').read_bytes())
    if record:
        atomic(w / 'workspace.json', {'schema_version': 1, 'workspace': str(w), 'python': str(py), 'skill_root': str(source)})
    run([py, '-B', source / 'scripts/da.py', '--workspace', w, 'doctor'])
    return py


def inventory(source, skill, w):
    source, skill, w = plain(source), plain(skill), plain(w)
    if within(skill, source) or within(source, skill):
        raise ValueError('Source and installation must be separate directories')
    if within(w, skill):
        raise ValueError('Workspace must be outside installed skill directory')
    manifest = read(source / 'delivery.json')
    files = [relative(x) for x in manifest['files']] + ['delivery.json']
    if len({x.lower() for x in files}) != len(files):
        raise ValueError('Duplicate manifest files')
    receipt = plain(skill / 'installed.json')
    old = read(receipt) if receipt.exists() else None
    if not old and skill.exists() and any(skill.iterdir()):
        raise ValueError('Existing installation has no hash receipt; inspect before adoption')
    previous = old.get('hashes', {}) if old else {}
    if old and (not isinstance(previous, dict) or not previous):
        raise ValueError('Invalid installation receipt')
    for rel, expected in previous.items():
        relative(rel)
        p = plain(skill / rel)
        if not p.is_file() or sha(p) != expected:
            raise ValueError('Old file changed: ' + rel)
    hashes = {}
    for rel in files:
        src, target = plain(source / rel), plain(skill / rel)
        if len(str(target)) > 160:
            raise ValueError('Installation path exceeds 160 characters')
        if not src.is_file():
            raise ValueError('Missing release file: ' + rel)
        hashes[rel] = sha(src)
        if target.exists():
            actual = sha(target)
            expected = previous.get(rel)
            if not expected and old and rel == 'delivery.json':
                if actual in manifest.get('previous_manifests', {}).get(old['version'], []):
                    expected = actual
            if actual != hashes[rel] and actual != expected:
                raise ValueError('Local modification conflict: ' + rel)
    return manifest, hashes, old, sorted(set(previous) - set(files))


def install(w, skill, conda, source=SOURCE, prepare_fn=prepare):
    source, skill, w = plain(source), plain(skill), plain(w)
    manifest, hashes, old, retired = inventory(source, skill, w)
    # Fail on user changes before environment preparation; repeat after it to catch intervening edits.
    py = prepare_fn(w, conda, source, record=False)
    manifest, hashes, old, retired = inventory(source, skill, w)
    backup = plain(w / 'backups' / ('install-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:6]))
    if within(backup, skill) or (skill.parent.name.lower() == 'skills' and within(backup, skill.parent)):
        raise ValueError('Backup must be outside the skill discovery directory')
    affected = [skill / rel for rel in sorted(set(hashes) | set(retired))]
    affected += [skill / 'installed.json', w / 'agent-context.json', w / 'workspace.json']
    approved = {p: sha(p) if p.is_file() else None for p in affected}
    # Recheck receipt-owned content before capturing rollback snapshots.
    for rel, expected in (old or {}).get('hashes', {}).items():
        if approved[skill / rel] != expected:
            raise ValueError('Old file changed before backup: ' + rel)
    snapshots = {}
    backup.mkdir(parents=True)
    for n, p in enumerate(affected):
        plain(p)
        if p.exists():
            saved = backup / ('skill' if within(p, skill) else 'workspace') / (p.relative_to(skill) if within(p, skill) else p.name)
            if len(str(saved)) > 160:
                raise ValueError("Backup path exceeds 160 characters; choose a shorter workspace")
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, saved)
            if sha(saved) != approved[p] or sha(p) != approved[p]:
                raise ValueError('File changed during backup: ' + str(p))
            snapshots[p] = saved
        else:
            snapshots[p] = None
    touched = []
    try:
        for rel in hashes:
            target = plain(skill / rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and sha(target) == hashes[rel]:
                continue
            if sha(source / rel) != hashes[rel]:
                raise ValueError('Release source changed: ' + rel)
            saved = snapshots[target]
            if (saved is None and target.exists()) or (saved is not None and (not target.exists() or sha(target) != sha(saved))):
                raise ValueError('Target changed during installation: ' + rel)
            # Record before copy so even a partial write is restored.
            touched.append(target)
            shutil.copy2(source / rel, target)
        for rel in retired:
            target = plain(skill / rel)
            if sha(target) != old['hashes'][rel]:
                raise ValueError('Retired file changed: ' + rel)
            target.unlink()
            touched.append(target)
        receipt = skill / 'installed.json'
        touched.append(receipt)
        atomic(receipt, {'schema_version': 1, 'version': manifest['version'], 'hashes': hashes,
                         'workspace': str(w), 'python': str(py)})
        workspace_record = w / 'workspace.json'
        touched.append(workspace_record)
        atomic(workspace_record, {'schema_version': 1, 'workspace': str(w), 'python': str(py), 'skill_root': str(skill)})
        ctx = w / 'agent-context.json'
        touched.append(ctx)
        atomic(ctx, {'schema_version': 1, 'skill_version': manifest['version'], 'workspace': str(w),
                    'python': str(py), 'skill_root': str(skill), 'documentation_index': str(skill / 'docs/agent/index.json'),
                    'observations': str(w / 'onboarding.json'), 'updated_at': datetime.now(timezone.utc).isoformat(),
                    'resume_rule': 'Read live status, requests.json and pending cache records; historical checks are not current health.'})
    except Exception as exc:
        errors = []
        for p in reversed(touched):
            try:
                plain(p)
                saved = snapshots[p]
                if saved is None:
                    if p.exists():
                        p.unlink()
                elif not p.exists() or sha(p) != sha(saved):
                    p.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(saved, p)
            except Exception as rollback_error:
                errors.append({'path': str(p), 'reason': str(rollback_error)})
        atomic(backup / 'recovery.json', {'status': 'rollback_pending' if errors else 'rolled_back',
                                        'error': str(exc), 'rollback_errors': errors})
        raise RuntimeError('Install failed; ' + ('rollback needs attention' if errors else 'files restored') + '; backup: ' + str(backup)) from exc
    return {'status': 'installed', 'version': manifest['version'], 'skill_dir': str(skill), 'workspace': str(w),
            'python': str(py), 'backup': str(backup), 'retired_files': retired,
            'next': 'Read AGENT_INSTALL.md and run onboard --check; verify host capabilities separately.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['install', 'setup'])
    parser.add_argument('--workspace')
    parser.add_argument('--skill-dir')
    parser.add_argument('--host', choices=['codex', 'workbuddy'], default='codex')
    parser.add_argument('--conda', required=True, help='Conda executable discovered by the shell launcher')
    args = parser.parse_args()
    if os.name != 'nt':
        parser.error('Windows PowerShell or Git Bash is required for this release')
    if sys.version_info < (3, 10):
        parser.error('Conda base Python 3.10+ required; see ' + CONDA_GUIDE)
    conda = plain(args.conda)
    if not conda.is_file():
        parser.error('Conda executable missing; see ' + CONDA_GUIDE)
    w = workspace_path(args.workspace)
    if args.mode == 'install':
        default_skill = w / '.codebuddy/skills/douyin-agent' if args.host == 'workbuddy' else Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills/douyin-agent'
        skill = plain(args.skill_dir or str(default_skill))
        result = install(w, skill, conda)
    else:
        if args.skill_dir:
            parser.error('--skill-dir applies only to install')
        result = {'status': 'prepared', 'workspace': str(w), 'python': str(prepare(w, conda))}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
