import pathlib
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task2/app.py'))
f = _load(pathlib.Path('fixed/task2/app.py'))

def test_reflected_xss_vuln():
    v.app.config['TESTING'] = True
    c = v.app.test_client()
    payload = '<script>document.title="XSS"</script>'
    rv = c.get('/search?q=' + payload)
    assert payload.encode() in rv.data

def test_reflected_xss_fixed_no_raw_script():
    f.app.config['TESTING'] = True
    c = f.app.test_client()
    payload = '<script>document.title="XSS"</script>'
    rv = c.get('/search?q=' + payload)
    assert b'<script>' not in rv.data
