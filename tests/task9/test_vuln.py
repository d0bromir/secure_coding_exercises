import subprocess
import shutil
import sys
from pathlib import Path
import pytest

# Resolve repo root reliably (tests/task9/<this file> -> parents[2] = repo root)
REPO_ROOT = Path(__file__).resolve().parents[2]

def build_and_run(src: Path, exe: Path, arg: str) -> bytes:
    src = src.resolve()
    exe = exe.resolve()
    # compile
    res = subprocess.run(['gcc', str(src), '-o', str(exe)], capture_output=True, text=True)
    if res.returncode != 0:
        pytest.fail(f"gcc failed\ncmd: {res.args}\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}")
    # run
    p = subprocess.run([str(exe), arg], capture_output=True)
    return p.stdout

def test_print_memory_content_vuln(tmp_path):
    if shutil.which("gcc") is None:
        pytest.skip("gcc not found, skipping C compile tests")

    src = REPO_ROOT / 'vulnerable' / 'task9' / 'app.c'
    assert src.exists(), f"Source file not found: {src}"

    exe_name = 'app.exe' if sys.platform.startswith('win') else 'app'
    exe = tmp_path / exe_name

    out = build_and_run(src, exe, '%x %x %x %x %x %x %x %x %x')
    assert isinstance(out, (bytes, bytearray))
    assert len(out) > 0
    assert out != b'%x %x %x %x %x %x %x %x %x'

def test_print_same_string_fixed(tmp_path):
    if shutil.which("gcc") is None:
        pytest.skip("gcc not found, skipping C compile tests")

    src = REPO_ROOT / 'fixed' / 'task9' / 'app.c'
    assert src.exists(), f"Source file not found: {src}"

    exe_name = 'app.exe' if sys.platform.startswith('win') else 'app'
    exe = tmp_path / exe_name

    out = build_and_run(src, exe, '%x %x %x %x %x %x %x %x %x')
    assert isinstance(out, (bytes, bytearray))
    assert len(out) > 0
    assert out == b'%x %x %x %x %x %x %x %x %x'
