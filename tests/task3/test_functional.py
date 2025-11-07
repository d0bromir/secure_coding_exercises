import pathlib, os
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task3/app.py'))
f = _load(pathlib.Path('fixed/task3/app.py'))

def test_functional_vuln(tmp_path):
    p = tmp_path
    for i in range(2):
        (p / f'file{i}.txt').write_text('hello')
    cwd = os.getcwd()
    os.chdir(p)
    try:
        v.compress('*.txt', out='o.tar.gz')
        assert os.path.exists('o.tar.gz')
    finally:
        os.chdir(cwd)

def test_functional_fixed(tmp_path):
    p = tmp_path
    for i in range(2):
        (p / f'file{i}.txt').write_text('hello')
    cwd = os.getcwd()
    os.chdir(p)
    try:
        f.compress('*.txt', out='o2.tar.gz')
        assert os.path.exists('o2.tar.gz')
    finally:
        os.chdir(cwd)
