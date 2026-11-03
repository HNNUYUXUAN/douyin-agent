"""Safely unpack a task's image ZIP; ordering still requires host verification."""
import argparse
import hashlib
import io
import json
import re
import stat
import warnings
import zipfile
from pathlib import Path, PurePosixPath
from PIL import Image

MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
FORMATS = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp', 'BMP': '.bmp'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unpack(archive, workspace, output, expected):
    archive = Path(archive).resolve(strict=True)
    workspace = Path(workspace).resolve(strict=True)
    raw_output = Path(output).absolute()
    if any(p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction())
           for p in [raw_output, *raw_output.parents]):
        raise ValueError('Output cannot cross a link or junction')
    output = raw_output.resolve()
    relative = output.relative_to(workspace)
    if not relative.parts or output.exists() or not 1 <= expected <= 100:
        raise ValueError('Use a new workspace subdirectory and 1..100 expected images')
    if len(str(output / 'manifest.json')) > 160 or any(
            not re.fullmatch(r'[A-Za-z0-9_.-]+', part) for part in relative.parts):
        raise ValueError('Use short ASCII output paths (at most 160 characters)')
    if archive.stat().st_size > MAX_TOTAL:
        raise ValueError('Archive too large')
    extracted = []
    with zipfile.ZipFile(archive) as z:
        entries = z.infolist()
        if len(entries) > 200:
            raise ValueError('Too many archive entries')
        names = set()
        total = 0
        for item in entries:
            name = item.orig_filename
            path = PurePosixPath(name)
            if (not name or path.is_absolute() or '..' in path.parts or '\\' in name
                    or ':' in name or any(ord(c) < 32 for c in name)
                    or name.casefold() in names):
                raise ValueError('Unsafe or duplicate archive path')
            names.add(name.casefold())
            mode = item.external_attr >> 16
            if stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError('Archive links and special files are forbidden')
            if item.flag_bits & 1:
                raise ValueError('Encrypted archives are not supported')
            if item.is_dir():
                continue
            total += item.file_size
            if (item.file_size > MAX_FILE or total > MAX_TOTAL or
                    item.file_size > max(1, item.compress_size) * 1000):
                raise ValueError('Archive expansion limit exceeded')
            if path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}:
                raise ValueError('Image-only archive required')
            with z.open(item) as f:
                data = f.read(MAX_FILE + 1)
            if len(data) != item.file_size or len(data) > MAX_FILE:
                raise ValueError('Invalid decompressed size')
            with warnings.catch_warnings():
                warnings.simplefilter('error', Image.DecompressionBombWarning)
                with Image.open(io.BytesIO(data)) as im:
                    fmt, size = im.format, im.size
                    if fmt not in FORMATS or size[0] * size[1] > 25_000_000:
                        raise ValueError('Unsupported image or image too large')
                    im.verify()
                with Image.open(io.BytesIO(data)) as im:
                    im.load()
            extracted.append((name, data, FORMATS[fmt], size))
    if len(extracted) != expected:
        raise ValueError(f'Expected {expected} images, found {len(extracted)}')
    extracted.sort(key=lambda row: [int(s) if s.isdigit() else s.casefold()
                                   for s in re.split(r'(\d+)', row[0])])
    manifest = {'schema_version': 1, 'archive': {'path': str(archive),
                'sha256': digest(archive.read_bytes())}, 'expected_images': expected,
                'order_basis': 'natural_filename_order_requires_host_verification',
                'order_verified': False, 'images': []}
    # Validate every entry before creating any output. Never extract archive paths.
    output.mkdir(parents=True, exist_ok=False)
    created = []
    try:
        for i, (original, data, suffix, size) in enumerate(extracted, 1):
            target = output / f'i{i:03}{suffix}'
            with target.open('xb') as f:
                created.append(target)
                f.write(data)
            manifest['images'].append({'index': i, 'archive_entry': original,
                'path': str(target), 'sha256': digest(data), 'width': size[0], 'height': size[1]})
        target = output / 'manifest.json'
        with target.open('x', encoding='utf-8') as f:
            created.append(target)
            json.dump(manifest, f, ensure_ascii=False, indent=2)
    except Exception:
        for p in created:
            p.unlink(missing_ok=True)
        output.rmdir()
        raise
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', required=True)
    p.add_argument('--workspace', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--expected-images', type=int, required=True)
    a = p.parse_args()
    result = unpack(a.archive, a.workspace, a.output, a.expected_images)
    print(json.dumps({'manifest': str(Path(a.output).resolve() / 'manifest.json'),
        'images': len(result['images']), 'order_verified': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
