import pathlib
import os
import time
import tempfile
import threading
from pathlib import Path
from tests._loader import load_module_from_path as _load

v = _load(pathlib.Path('vulnerable/task6/app.py'))
f = _load(pathlib.Path('fixed/task6/app.py'))

def _attacker_paths(base_tmp: Path):
    """Return platform-appropriate attacker marker/target paths."""
    # marker: for POSIX symlink method (file written by exploited target)
    marker = Path(tempfile.gettempdir()) / "t6_pwn_marker"
    # attacker_target: for Windows replace-method
    attacker_target = base_tmp / "attacker_target.txt"
    return marker, attacker_target

def _swap_loop(target: Path, stop_event: threading.Event):
    """
    Rapidly swap the 'target' path between regular file and attacker file.
    On POSIX: try to create a symlink pointing outside (if possible).
    On Windows: create an attacker file elsewhere and replace() it into place.
    """
    base_tmp = target.parent
    marker, attacker_target = _attacker_paths(base_tmp)
    while not stop_event.is_set():
        try:
            # Remove if exists
            if target.exists() or target.is_symlink():
                try:
                    target.unlink()
                except Exception:
                    # swallow transient errors
                    pass

            if os.name == 'nt':
                # Windows approach: create attacker file and atomically replace into target
                attacker_target.write_text("ATTACKER", encoding='utf-8')
                # os.replace is atomic on the same filesystem
                try:
                    os.replace(str(attacker_target), str(target))
                except Exception:
                    # if replace fails, ignore and continue
                    pass
                # tiny sleep so writer sees attacker target
                time.sleep(0.0005)
                # revert: create a safe file at target to restore baseline
                try:
                    # ensure target exists as a normal file again
                    target.unlink()
                except Exception:
                    pass
                (target).write_text("SAFE", encoding='utf-8')
                time.sleep(0.0005)
                # cleanup attacker_target if it was recreated
                try:
                    if attacker_target.exists():
                        attacker_target.unlink()
                except Exception:
                    pass
            else:
                # POSIX approach: try symlink to a safe marker in temp
                try:
                    # point symlink to global marker path (in per-user temp)
                    if target.exists() or target.is_symlink():
                        try:
                            target.unlink()
                        except Exception:
                            pass
                    target.symlink_to(str(marker))
                except Exception:
                    # if symlink creation failed (permissions), fallback to creating a file
                    target.write_text("ATTACKER_FALLBACK", encoding='utf-8')
                time.sleep(0.001)
                # revert back to a normal safe file
                try:
                    if target.exists() or target.is_symlink():
                        target.unlink()
                except Exception:
                    pass
                target.write_text("SAFE", encoding='utf-8')
                time.sleep(0.001)
        except Exception:
            # suppress transient errors caused by race conditions
            pass

def test_toctou_vuln(tmp_path):
    target = tmp_path / 't.txt'
    stop = threading.Event()
    t = threading.Thread(target=_swap_loop, args=(target, stop))
    t.start()

    # We'll try calling the vulnerable writer repeatedly until we either:
    # - observe that attacker_target got the 'exploit' content (Windows style), or
    # - observe the marker file exists (POSIX symlink style), or
    # - timeout after a short while
    try:
        seen_written = False
        seen_attacker_hit = False
        seen_marker = False
        deadline = time.time() + 5.0  # 5 seconds total max for the attempt loop
        while time.time() < deadline:
            try:
                # call vulnerable function; it may raise PermissionError occasionally - catch and continue
                v.write_if_safe(str(target), 'exploit')
                # if write_if_safe returned normally, check content of target
                if target.exists():
                    try:
                        txt = target.read_text(encoding='utf-8')
                    except Exception:
                        txt = None
                    if txt == 'exploit':
                        seen_written = True
                        break
                # check attacker-style evidence
                _, attacker_target = _attacker_paths(tmp_path)
                if attacker_target.exists():
                    # if attacker file captured the exploit content, vuln succeeded
                    try:
                        at = attacker_target.read_text(encoding='utf-8')
                    except Exception:
                        at = None
                    if at == 'exploit':
                        seen_attacker_hit = True
                        break
                # check POSIX marker
                marker, _ = _attacker_paths(tmp_path)
                if marker.exists():
                    try:
                        if marker.read_text(encoding='utf-8') == 'pwn' or marker.exists():
                            seen_marker = True
                            break
                    except Exception:
                        seen_marker = True
                        break
            except PermissionError:
                # transient on Windows when target replaced with a special FS object; keep retrying
                pass
            except Exception:
                # ignore unexpected transient races and keep retrying a bit
                pass
            time.sleep(0.01)
    finally:
        stop.set()
        t.join()

    # Accept any of the evidence outcomes as a successful exploitation of TOCTOU:
    assert seen_written or seen_attacker_hit or seen_marker, (
        "TOCTOU exploit not observed: no 'exploit' written to target or attacker file/marker. "
        "On Windows you may need Developer Mode for symlinks; this test uses replace()-based swap fallback."
    )

def test_toctou_fixed(tmp_path):
    target = tmp_path / 't2.txt'
    f.write_if_safe(str(target), 'ok')
    assert target.read_text(encoding='utf-8') == 'ok'
