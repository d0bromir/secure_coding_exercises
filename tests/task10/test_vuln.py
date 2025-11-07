import pathlib
import re

# Current file = tests/task10/test_vuln.py
# Go up до репо-корена
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
REQ_FILE_V = REPO_ROOT / "vulnerable/task10/requirements.txt"
REQ_FILE_F = REPO_ROOT / "fixed/task10/requirements.txt"

_VERSION_RE = re.compile(r'(?im)^\s*flask==\s*([0-9]+(?:\.[0-9]+)*)\s*$')

def _version_to_tuple(vstr, parts=3):
    """
    Convert '1.2.3' -> (1,2,3), pad with zeros to `parts`.
    Ignore any pre-release suffixes like '1.2.3rc1' by keeping numeric prefix.
    """
    # keep only the numeric prefix like '1.2.3' from '1.2.3rc1' or '1.2.3-alpha'
    m = re.match(r'^([0-9]+(?:\.[0-9]+)*)', vstr)
    if not m:
        return None
    nums = [int(x) for x in m.group(1).split('.')]
    # pad to desired length
    nums += [0] * (parts - len(nums))
    return tuple(nums[:parts])

def test_dependency_scan_marker_vulnerable():
    assert REQ_FILE_V.exists(), f"requirements.txt not found at {REQ_FILE_V}"
    content = REQ_FILE_V.read_text(encoding="utf-8")

    m = _VERSION_RE.search(content)
    assert m, "Flask==<version> entry not found in requirements.txt"

    verstr = m.group(1)
    vtuple = _version_to_tuple(verstr)
    assert vtuple is not None, f"Could not parse Flask version '{verstr}'"

    # Check if version < 1.0.0
    if vtuple < (1, 0, 0):
        # vulnerable: version is older than 1.0.0
        assert True
    else:
        # not vulnerable
        raise AssertionError(f"Flask version is {verstr} (>= 1.0.0) — test expects version < 1.0.0 for the vulnerable case")

def test_dependency_scan_marker_fixed():
    assert REQ_FILE_F.exists(), f"requirements.txt not found at {REQ_FILE_F}"
    content = REQ_FILE_F.read_text(encoding="utf-8")

    m = _VERSION_RE.search(content)
    assert m, "Flask==<version> entry not found in requirements.txt"

    verstr = m.group(1)
    vtuple = _version_to_tuple(verstr)
    assert vtuple is not None, f"Could not parse Flask version '{verstr}'"

    # Check if version >= 1.0.0
    if vtuple >= (1, 0, 0):
        # not vulnerable:
        assert True
    else:
        # not vulnerable
        raise AssertionError(
            f"Flask version is {verstr} (<= 1.0.0) — test expects version > 1.0.0 for the fixed case")
