import subprocess
import shutil
import sys
from pathlib import Path
import pytest

# Корен на репото: tests/task9/<този файл> -> ../.. = repo root
REPO_ROOT = Path(__file__).resolve().parents[2]

def build_and_run(src: Path, exe: Path, arg: str) -> bytes:
    src = src.resolve()
    exe = exe.resolve()

    # Компилация с видима диагностика при грешка
    res = subprocess.run(['gcc', str(src), '-o', str(exe)],
                         capture_output=True, text=True)
    if res.returncode != 0:
        pytest.fail(f"gcc failed\ncmd: {res.args}\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}")

    # Стартиране
    p = subprocess.run([str(exe), arg], capture_output=True)
    return p.stdout

def test_functional_vuln(tmp_path):
    # Пропусни теста, ако gcc липсва
    if shutil.which("gcc") is None:
        pytest.skip("gcc not found, skipping C compile tests")

    src = REPO_ROOT / 'vulnerable' / 'task9' / 'app.c'
    assert src.exists(), f"Source file not found: {src}"

    exe_name = 'app.exe' if sys.platform.startswith('win') else 'app'
    exe = tmp_path / exe_name

    out = build_and_run(src, exe, 'hello')
    assert isinstance(out, (bytes, bytearray))
    assert out == b'hello'

def test_functional_fixed(tmp_path):
    # Пропусни теста, ако gcc липсва
    if shutil.which("gcc") is None:
        pytest.skip("gcc not found, skipping C compile tests")

    src = REPO_ROOT / 'fixed' / 'task9' / 'app.c'
    assert src.exists(), f"Source file not found: {src}"

    exe_name = 'app.exe' if sys.platform.startswith('win') else 'app'
    exe = tmp_path / exe_name

    out = build_and_run(src, exe, 'hello')
    assert isinstance(out, (bytes, bytearray))
    assert out == b'hello'