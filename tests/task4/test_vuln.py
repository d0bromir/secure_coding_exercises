import pathlib
import os
import pickle
import tempfile
from pathlib import Path
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task4/app.py'))
f = _load(pathlib.Path('fixed/task4/app.py'))

class Evil:
    def run(self):
        # write marker into per-user temp dir
        p = Path(tempfile.gettempdir()) / "pickle_pwn"
        p.write_text("pwn", encoding="utf-8")

def _marker_path():
    return Path(tempfile.gettempdir()) / "pickle_pwn"

def test_pickle_rce_vuln():
    marker = _marker_path()
    # ensure old marker removed
    if marker.exists():
        marker.unlink()
    # save a pickle that will execute on load in the vulnerable implementation
    v.save(Evil())
    # call loader that uses pickle.loads and (in vuln) will execute Evil.run()
    v.load_and_use()
    assert marker.exists(), f"expected marker at {marker}"
    marker.unlink()

def test_pickle_rce_fixed_no_rce():
    # write a pickle file where the fixed impl expects JSON
    fixed_file = Path(tempfile.gettempdir()) / "fixed_json.dat"
    try:
        # write binary pickle (should not be executed by fixed JSON loader)
        with open(fixed_file, "wb") as fh:
            fh.write(pickle.dumps(Evil()))
        # calling fixed loader should either raise or safely ignore; in any case no marker should appear
        try:
            f.load_and_use()
        except Exception:
            # expected: fixed loader may raise when reading a non-JSON file
            pass
        assert not _marker_path().exists(), "marker must not be created by fixed loader"
    finally:
        if fixed_file.exists():
            fixed_file.unlink()
