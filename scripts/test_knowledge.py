import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import knowledge as kb
from media_tools import configure


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='dak-')
        self.w = Path(self.tmp.name)
        (self.w / 'proof.json').write_text('{"result":"synthetic"}')
        self.data = {'id': 'browser-test', 'title': 'Browser verification', 'symptom': 'Extension installed; bridge unknown',
                     'action': 'Read actual bridge status', 'result': 'Synthetic observation', 'verification': 'Synthetic only',
                     'keywords': ['WorkBuddy', '连接'], 'sources': ['proof.json']}
        self.input = self.w / 'case.json'

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        self.input.write_text(json.dumps(self.data), encoding='utf-8')
        return kb.record(self.w, self.input)

    def test_record_search_reindex_and_no_overwrite(self):
        r = self.save(); case = Path(r['case']); content = case.read_bytes()
        self.assertEqual(r['cases'], 1)
        meta, body = kb.document(case); self.assertEqual(meta['status'], 'draft')
        self.assertEqual(len(kb.search([('private', self.w / 'knowledge-private')], '连接')), 1)
        (self.w / 'knowledge-private/index.md').unlink()
        self.assertEqual(kb.reindex(self.w / 'knowledge-private')['cases'], 1)
        with self.assertRaisesRegex(ValueError, 'already exists'): self.save()
        self.assertEqual(case.read_bytes(), content)

    def test_search_missing_private_directory_is_read_only(self):
        before = set(self.w.iterdir())
        self.assertEqual(kb.search([('private', self.w / 'knowledge-private')], 'anything'), [])
        self.assertEqual(set(self.w.iterdir()), before)

    def test_public_okf_profile_and_unknown_type(self):
        self.assertGreaterEqual(len(kb.concepts(kb.BUNDLE)), 8)
        kb.atomic(self.w / 'unknown.md', '---\n{"type":"New Producer Type"}\n---\nBody\n')
        self.assertEqual(kb.document(self.w / 'unknown.md')[0]['type'], 'New Producer Type')

    def test_private_evidence_escape_and_credentials_rejected(self):
        for value in ['../outside.json', 'https://example.com/?token=secret', 'https://user:pass@example.com/']:
            self.data['sources'] = [value]
            with self.assertRaises((ValueError, OSError)): self.save()
        self.data['sources'] = ['proof.json']; self.data['action'] = 'api_key=secret'
        with self.assertRaises(ValueError): self.save()
        self.assertFalse((self.w / 'knowledge-private/cases/browser-test.md').exists())

    def test_title_markdown_rejected(self):
        with self.assertRaisesRegex(ValueError, '160'):
            kb.plain(self.w / ('a' * 160))
        self.data['title'] = '[instruction](https://example.com)'
        with self.assertRaises(ValueError): self.save()

    def test_media_pair_process_path_without_global_install(self):
        folder = self.w / 'tools/ffmpeg/bin'; folder.mkdir(parents=True)
        with patch.dict(os.environ, {'PATH': 'BASE'}):
            (folder / 'ffmpeg.exe').write_bytes(b'fixture')
            self.assertIsNone(configure(self.w))
            self.assertEqual(os.environ['PATH'], 'BASE')
            (folder / 'ffprobe.exe').write_bytes(b'fixture')
            self.assertEqual(configure(self.w), str(folder))
            configure(self.w)
            self.assertEqual(os.environ['PATH'].count(str(folder)), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
