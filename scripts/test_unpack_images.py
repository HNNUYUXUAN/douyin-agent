import io
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path
from PIL import Image
from unpack_images import unpack


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.w = Path(self.tmp.name)
        b = io.BytesIO()
        Image.new('RGB', (12, 20), 'red').save(b, format='PNG')
        self.png = b.getvalue()

    def tearDown(self):
        self.tmp.cleanup()

    def archive(self, entries):
        p = self.w / 'in.zip'
        with zipfile.ZipFile(p, 'w') as z:
            for name, data in entries:
                if isinstance(name, str):
                    item = zipfile.ZipInfo()
                    item.filename = name
                    name = item
                z.writestr(name, data)
        return p

    def test_decodes_renames_and_natural_order_without_claiming_identity(self):
        p = self.archive([('images/10.jpg', self.png), ('images/2.jpg', self.png)])
        r = unpack(p, self.w, self.w / 'out', 2)
        self.assertEqual(r['images'][0]['archive_entry'], 'images/2.jpg')
        self.assertEqual(Path(r['images'][0]['path']).name, 'i001.png')
        self.assertFalse(r['order_verified'])
        self.assertTrue(p.exists())

    def test_rejects_unsafe_entries_before_output(self):
        for name in ['../evil.png', '/evil.png', 'C:/evil.png', 'x\\evil.png', 'run.exe']:
            with self.subTest(name=name):
                p = self.archive([(name, self.png)])
                with self.assertRaises(ValueError):
                    unpack(p, self.w, self.w / 'out', 1)
                self.assertFalse((self.w / 'out').exists())

    def test_rejects_symlink_count_and_fake_image(self):
        link = zipfile.ZipInfo('link.png')
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        for entries, count in [([(link, b'target')], 1), ([('1.png', self.png)], 2),
                                ([('1.png', b'not an image')], 1)]:
            p = self.archive(entries)
            with self.assertRaises((ValueError, OSError)):
                unpack(p, self.w, self.w / 'out', count)
            self.assertFalse((self.w / 'out').exists())

    def test_preserves_existing_output(self):
        out = self.w / 'out'
        out.mkdir()
        (out / 'keep.md').write_text('keep')
        p = self.archive([('1.png', self.png)])
        with self.assertRaises(ValueError):
            unpack(p, self.w, out, 1)
        self.assertEqual((out / 'keep.md').read_text(), 'keep')


if __name__ == '__main__':
    unittest.main()
