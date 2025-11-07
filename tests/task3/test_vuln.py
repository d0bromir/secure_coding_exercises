import pathlib
import os
import tempfile
from pathlib import Path
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task3/app.py'))
f = _load(pathlib.Path('fixed/task3/app.py'))

def _pwn_marker_path():
    # per-user temp (portable)
    return Path(tempfile.gettempdir()) / "pwn_marker"

def test_command_injection_vuln(tmp_path):
    p = tmp_path
    (p / 'file.txt').write_text('x', encoding='utf-8')
    cwd = os.getcwd()
    os.chdir(p)
    try:
        marker = _pwn_marker_path()
        # ensure old marker removed
        if marker.exists():
            marker.unlink()
        # use an echo redirect that works on common shells; quote the path to be safe
        v.compress(f'file.txt; echo VULN > \"{marker}\"', out='o.tar.gz')
        assert marker.exists()
        marker.unlink()
    finally:
        os.chdir(cwd)

def test_command_injection_fixed_no_inject(tmp_path):
    p = tmp_path
    (p / 'file.txt').write_text('x', encoding='utf-8')
    cwd = os.getcwd()
    os.chdir(p)
    try:
        marker = _pwn_marker_path()
        if marker.exists():
            marker.unlink()
        f.compress(f'file.txt; echo VULN > \"{marker}\"', out='o2.tar.gz')
        assert not marker.exists()
    finally:
        os.chdir(cwd)
