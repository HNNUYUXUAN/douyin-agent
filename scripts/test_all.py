"""Maintenance-only offline suite, using the production workspace FFmpeg resolver."""
import argparse, os, shutil, subprocess, sys
from pathlib import Path
from media_tools import configure

TESTS=('test_da.py','test_onboarding.py','test_unpack_images.py','test_installer.py',
       'test_knowledge.py','test_browsing.py','test_v25.py','test_v251.py')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',required=True,type=Path);a=p.parse_args()
    configure(a.workspace.resolve())
    missing=[x for x in ('ffmpeg','ffprobe') if not shutil.which(x)]
    if missing: p.error('Missing '+', '.join(missing)+'; prepare workspace tools/ffmpeg/bin before maintenance tests')
    failed=[]
    for name in TESTS:
        result=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name(name))],env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1'))
        if result.returncode: failed.append(name)
    if failed: print('Failed: '+', '.join(failed),file=sys.stderr)
    return bool(failed)

if __name__=='__main__':sys.exit(main())
