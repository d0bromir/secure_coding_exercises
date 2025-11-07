import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task6/app.py'))
f = _load(pathlib.Path('fixed/task6/app.py'))

def test_functional_vuln(tmp_path):
    p = tmp_path / 'f.txt'
    v.write_if_safe(str(p), 'ok')
    assert p.read_text() == 'ok'

def test_functional_fixed(tmp_path):
    p = tmp_path / 'f2.txt'
    f.write_if_safe(str(p), 'ok2')
    assert p.read_text() == 'ok2'
