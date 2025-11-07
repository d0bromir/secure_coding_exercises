import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task1/app.py'))
f = _load(pathlib.Path('fixed/task1/app.py'))

def test_sqli_vulnerable():
    v.init()
    assert v.login("' OR '1'='1' -- ", "x") is True

def test_sqli_fixed_not_bypass():
    f.init()
    assert f.login("' OR '1'='1' -- ", "x") is False
