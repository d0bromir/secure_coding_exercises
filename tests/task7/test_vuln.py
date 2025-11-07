import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task7/app.py'))
f = _load(pathlib.Path('fixed/task7/app.py'))

def test_authz_vuln_allows_other_user():
    v.app.config['TESTING'] = True
    c = v.app.test_client()
    rv = c.get('/user/1/data', headers={'X-User-ID':'2'})
    assert rv.status_code == 200
    assert b'secret1' in rv.data

def test_authz_fixed_blocks_other_user():
    f.app.config['TESTING'] = True
    c = f.app.test_client()
    rv = c.get('/user/1/data', headers={'X-User-ID':'2'})
    assert rv.status_code == 403
