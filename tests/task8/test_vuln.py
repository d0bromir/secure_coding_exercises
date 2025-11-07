import pathlib, tempfile, os
from tests._loader import load_module_from_path as _load

v=_load(pathlib.Path('vulnerable/task8/app.py'))
f=_load(pathlib.Path('fixed/task8/app.py'))

def test_logs_contain_password_vuln():
    v.process_login('alice','mypw123')
    log=os.path.join(tempfile.gettempdir(),'app.log')
    assert os.path.exists(log)
    assert 'mypw123' in open(log,encoding='utf-8').read()

def test_logs_masked_fixed():
    f.process_login('alice','mypw123')
    log=os.path.join(tempfile.gettempdir(),'app.log')
    assert os.path.exists(log)
    assert 'mypw123' not in open(log,encoding='utf-8').read()
