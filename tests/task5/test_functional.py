import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task5/app.py'))
f = _load(pathlib.Path('fixed/task5/app.py'))

def test_functional_vuln():
    pt = b'YELLOW_SUBMARINEYELLOW_SUBMARINE'
    key, nonce, c = f.encrypt(pt)
    ct = f.decrypt(key, nonce, c)
    assert pt == ct

def test_functional_fixed():
    pt = b'YELLOW_SUBMARINEYELLOW_SUBMARINE'
    key, nonce, c = f.encrypt(pt)
    ct = f.decrypt(key, nonce, c)
    assert pt == ct
