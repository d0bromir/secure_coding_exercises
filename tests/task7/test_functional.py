import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task7/app.py'))
f = _load(pathlib.Path('fixed/task7/app.py'))

def test_functional_vuln_client():
    v.app.config['TESTING'] = True
    c = v.app.test_client()
    rv = c.get('/user/1/data', headers={'X-User-ID':'1'})
    assert rv.status_code == 200

def test_functional_fixed_client():
    f.app.config['TESTING'] = True
    c = f.app.test_client()
    rv = c.get('/user/1/data', headers={'X-User-ID':'1'})
    assert rv.status_code == 200
