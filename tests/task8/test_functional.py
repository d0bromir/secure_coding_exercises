import pathlib, os
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task8/app.py'))
f = _load(pathlib.Path('fixed/task8/app.py'))

def test_functional_vuln(tmp_path):
    v.process_login('alice','wrong')
    assert True

def test_functional_fixed(tmp_path):
    f.process_login('alice','wrong')
    assert True
