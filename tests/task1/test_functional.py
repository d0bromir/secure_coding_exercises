import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task1/app.py'))
f = _load(pathlib.Path('fixed/task1/app.py'))

def test_functional_vulnerable():
    v.init()
    assert v.login('alice', 'alicepass') is True

def test_functional_fixed():
    f.init()
    assert f.login('alice', 'alicepass') is True
