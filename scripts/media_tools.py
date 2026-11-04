"""Enable a workspace-local portable FFmpeg pair without changing global PATH."""
import os
from pathlib import Path


def configure(workspace):
    directory = Path(workspace) / 'tools/ffmpeg/bin'
    if all((directory / name).is_file() for name in ('ffmpeg.exe', 'ffprobe.exe')):
        for p in (directory, *directory.parents):
            if p.is_symlink() or (p.exists() and getattr(p.lstat(), 'st_file_attributes', 0) & 0x400):
                raise ValueError('Linked local media tools are unsupported')
        parts = os.environ.get('PATH', '').split(os.pathsep)
        if str(directory) not in parts:
            os.environ['PATH'] = str(directory) + os.pathsep + os.environ.get('PATH', '')
        return str(directory)
    return None
