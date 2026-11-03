import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from datetime import datetime, timezone, timedelta
import onboarding

class OnboardingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.w=Path(self.tmp.name).resolve()
        self.script=Path(__file__).with_name('da.py')
    def tearDown(self): self.tmp.cleanup()
    def call(self,*args):
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1'); env.pop('VOLC_AGENT_API_KEY',None)
        return subprocess.run([sys.executable,'-B',str(self.script),'--workspace',str(self.w),*args],capture_output=True,text=True,encoding='utf-8',env=env)
    def snapshot(self):
        return {str(p.relative_to(self.w)):(p.read_bytes(),p.stat().st_mtime_ns) for p in self.w.rglob('*') if p.is_file()}
    def test_read_only_commands_do_not_create_or_change_files(self):
        (self.w/'.env').write_text('VOLC_AGENT_API_KEY=\n')
        for cmd in [('doctor',),('status',),('onboard','--check')]:
            before=self.snapshot(); r=self.call(*cmd)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr); self.assertEqual(before,self.snapshot())
        result=json.loads(r.stdout); self.assertFalse(result['local']['key_present']); self.assertFalse(result['cloud_verified_by_this_check'])
    def record(self,evidence='evidence.md',**overrides):
        value={'status':'passed','observed_at':(datetime.now(timezone.utc)-timedelta(seconds=5)).isoformat(),'evidence':evidence}; value.update(overrides)
        (self.w/'record.json').write_text(json.dumps({'schema_version':1,'checks':{'douyin_access':value}}))
        return self.call('onboard','--record',str(self.w/'record.json'))
    def test_explicit_record_and_private_context(self):
        (self.w/'evidence.md').write_text('Host observed public page')
        r=self.record(); self.assertEqual(r.returncode,0,r.stdout)
        result=json.loads(r.stdout); self.assertTrue(result['record_written']); self.assertFalse(result['browser_verified_by_this_check'])
        context=json.loads((self.w/'agent-context.json').read_text()); self.assertEqual(context['skill_version'],'2.1.0')
        self.assertTrue(Path(context['documentation_index']).is_file())
    def test_unsafe_receipts_never_persist(self):
        for evidence in ['../outside.md','https://example.com/?token=secret','https://user:pass@example.com/','data:image/png;base64,xyz','private.txt']:
            r=self.record(evidence); self.assertNotEqual(r.returncode,0,evidence)
            self.assertFalse((self.w/'onboarding.json').exists())
    def test_future_observation_rejected(self):
        r=self.record('https://www.douyin.com/',observed_at=(datetime.now(timezone.utc)+timedelta(days=1)).isoformat())
        self.assertNotEqual(r.returncode,0); self.assertFalse((self.w/'agent-context.json').exists())
    def test_missing_media_tools_are_reported_without_installing(self):
        with patch('onboarding.shutil.which',return_value=None):
            r=onboarding.onboard(self.w,SimpleNamespace(record=None),'2.1.0',lambda p: {},lambda *x:self.fail('unexpected write'),lambda w:{})
        self.assertFalse(r['local']['ffmpeg']); self.assertFalse(r['local']['ffprobe'])

if __name__=='__main__': unittest.main()
