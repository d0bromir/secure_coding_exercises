import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task4/app.py'))
f = _load(pathlib.Path('fixed/task4/app.py'))

def test_functional_vuln():
    v.save({'x':1})
    vres = v.load_and_use()
    assert isinstance(vres, dict) or vres is None

def test_functional_fixed():
    f.save({'x':1})
    fres = f.load_and_use()
    assert isinstance(fres, dict) or fres is None
