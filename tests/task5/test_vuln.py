import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task5/app.py'))
f = _load(pathlib.Path('fixed/task5/app.py'))

def test_ecb_pattern_leak():
    block = b'A'*16
    pt = block + block + b'B'*16
    key, nonce, ct = v.encrypt(pt)
    assert ct[0:16] == ct[16:32]

def test_fixed():
    block = b'A'*16
    pt = block + block + b'B'*16
    key, nonce, ct = f.encrypt(pt)
    assert ct[0:16] != ct[16:32]
