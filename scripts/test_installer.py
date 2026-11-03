import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import installer as ins


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='dai-')
        self.root = Path(self.tmp.name)
        self.src = self.root / 'src'
        self.skill = self.root / 'host/skills/da'
        self.w = self.root / 'ws'
        self.src.mkdir()
        self.w.mkdir()
        (self.w / '.env').write_text('PRIVATE_TEST_VALUE=keep\n')
        self.release({'a.md': 'a1', 'retired.md': 'old'}, '2.1.0')

    def tearDown(self):
        self.tmp.cleanup()

    def release(self, files, version='2.2.0'):
        for name, text in files.items():
            p = self.src / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding='utf-8')
        ins.atomic(self.src / 'delivery.json', {'version': version, 'files': list(files)})

    def prep(self, w, conda, source, record=True):
        self.assertFalse(record)
        return w / 'envs/runtime/python.exe'

    def install(self):
        return ins.install(self.w, self.skill, 'unused', self.src, self.prep)

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for base in (self.skill, self.w)
                for p in base.rglob('*') if p.is_file() and 'backups' not in p.parts}

    def test_fresh_repeat_and_actual_context(self):
        first = self.install()
        self.assertEqual(first['version'], '2.1.0')
        before = (self.w / '.env').read_bytes()
        self.install()
        for name in ['workspace.json', 'agent-context.json']:
            self.assertEqual(ins.read(self.w / name)['skill_root'], str(self.skill))
        self.assertEqual((self.w / '.env').read_bytes(), before)

    def test_upgrade_retires_only_owned_files(self):
        self.install()
        (self.skill / 'user.md').write_text('user')
        self.release({'a.md': 'a2', 'new.md': 'new'})
        result = self.install()
        self.assertEqual(result['retired_files'], ['retired.md'])
        self.assertFalse((self.skill / 'retired.md').exists())
        self.assertEqual((self.skill / 'user.md').read_text(), 'user')
        self.assertEqual((Path(result['backup']) / 'skill/retired.md').read_text(), 'old')

    def test_changed_retired_file_stops_before_prepare(self):
        self.install()
        (self.skill / 'retired.md').write_text('user edit')
        self.release({'a.md': 'a2'})
        with patch.object(ins, 'prepare', side_effect=AssertionError('must not run')):
            with self.assertRaisesRegex(ValueError, 'Old file changed'):
                self.install()
        self.assertEqual((self.skill / 'a.md').read_text(), 'a1')

    def test_partial_copy_failure_restores_all_files(self):
        self.install()
        old = self.snapshot()
        self.release({'a.md': 'a2', 'z.md': 'new'})
        original = shutil.copy2
        def fail(src, dst, *args, **kwargs):
            if Path(dst) == self.skill / 'z.md':
                Path(dst).write_text('partial')
                raise OSError('simulated interrupted write')
            return original(src, dst, *args, **kwargs)
        with patch.object(ins.shutil, 'copy2', side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, 'files restored'):
                self.install()
        self.assertEqual(old, self.snapshot())

    def test_context_failure_restores_retired_receipt_and_workspace(self):
        self.install()
        old = self.snapshot()
        self.release({'a.md': 'a2'})
        original = ins.atomic
        def fail(path, value):
            if path == self.w / 'agent-context.json':
                raise OSError('context write denied')
            return original(path, value)
        with patch.object(ins, 'atomic', side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, 'files restored'):
                self.install()
        self.assertEqual(old, self.snapshot())

    def test_concurrent_edit_is_preserved(self):
        self.install()
        self.release({'a.md': 'a2'})
        original = shutil.copy2
        def edit(src, dst, *args, **kwargs):
            result = original(src, dst, *args, **kwargs)
            if Path(dst).name == 'agent-context.json' and 'backups' in Path(dst).parts:
                (self.skill / 'a.md').write_text('concurrent user edit')
            return result
        with patch.object(ins.shutil, 'copy2', side_effect=edit):
            with self.assertRaisesRegex(RuntimeError, 'files restored'):
                self.install()
        self.assertEqual((self.skill / 'a.md').read_text(), 'concurrent user edit')

    @unittest.skipUnless(os.name == 'nt', 'Windows sharing semantics')
    def test_real_windows_lock_restores_prior_writes(self):
        import ctypes
        from ctypes import wintypes
        self.install()
        old = self.snapshot()
        self.release({'a.md': 'a2'})
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        kernel.CreateFileW.restype = wintypes.HANDLE
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.CreateFileW(str(self.skill / 'retired.md'), 0x80000000, 1, None, 3, 0, None)
        self.assertNotEqual(handle, ctypes.c_void_p(-1).value)
        try:
            with self.assertRaisesRegex(RuntimeError, 'files restored'):
                self.install()
            self.assertEqual(old, self.snapshot())
        finally:
            kernel.CloseHandle(handle)

    def test_edit_during_backup_is_preserved(self):
        self.install()
        self.release({'a.md': 'a2'})
        original = shutil.copy2
        def edit(src, dst, *args, **kwargs):
            if Path(src) == self.skill / 'a.md' and 'backups' in Path(dst).parts:
                Path(src).write_text('changed during snapshot')
            return original(src, dst, *args, **kwargs)
        with patch.object(ins.shutil, 'copy2', side_effect=edit):
            with self.assertRaisesRegex(ValueError, 'changed during backup'):
                self.install()
        self.assertEqual((self.skill / 'a.md').read_text(), 'changed during snapshot')

    def test_manifest_traversal_and_case_duplicates(self):
        for names in [['../outside.md'], ['a.md', 'A.md']]:
            ins.atomic(self.src / 'delivery.json', {'version': '2.2.0', 'files': names})
            with self.assertRaises(ValueError):
                self.install()
        self.assertFalse(self.skill.exists())

    def test_unknown_install_directory_is_protected(self):
        self.skill.mkdir(parents=True)
        (self.skill / 'user.md').write_text('user')
        with self.assertRaisesRegex(ValueError, 'no hash receipt'):
            self.install()

    def test_no_d_default_and_long_workspace(self):
        with patch.object(Path, 'is_dir', return_value=False):
            self.assertEqual(ins.default_workspace(), Path.home() / 'douyin-agent')
        with self.assertRaisesRegex(ValueError, 'shorter'):
            ins.workspace_path(str(self.root / ('x' * 90)))

    def test_receipt_path_tampering(self):
        self.install()
        p = self.skill / 'installed.json'
        receipt = ins.read(p)
        receipt['hashes']['../outside.md'] = '0' * 64
        ins.atomic(p, receipt)
        with self.assertRaisesRegex(ValueError, 'Unsafe manifest'):
            self.install()


if __name__ == '__main__':
    unittest.main(verbosity=2)
