import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task2/app.py'))
f = _load(pathlib.Path('fixed/task2/app.py'))

def test_functional_vuln():
    v.app.config['TESTING'] = True
    c = v.app.test_client()
    rv = c.get('/search?q=hello')
    assert b'Results for: hello' in rv.data

def test_functional_fixed():
    f.app.config['TESTING'] = True
    c = f.app.test_client()
    rv = c.get('/search?q=hello')
    assert b'Results for: hello' in rv.data
