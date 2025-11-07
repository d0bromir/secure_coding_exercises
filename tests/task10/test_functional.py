import pathlib
from tests._loader import load_module_from_path as _load

pv = _load(pathlib.Path('vulnerable/task10/app.py'))
pf = _load(pathlib.Path('fixed/task10/app.py'))

def test_functional_vuln():
    assert pv.greet().startswith('hello')

def test_functional_fixed():
    assert pf.greet().startswith('hello')
