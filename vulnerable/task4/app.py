import pickle
import tempfile
from pathlib import Path

# per-user temp path (portable)
DATAFILE = Path(tempfile.gettempdir()) / "vuln_pickle.dat"

def save(obj):
    DATAFILE.parent.mkdir(parents=True, exist_ok=True)
    # уязвимо: записваме pickle директно
    with open(DATAFILE, "wb") as fh:
        fh.write(pickle.dumps(obj))

def load_and_use():
    with open(DATAFILE, "rb") as fh:
        obj = pickle.loads(fh.read())
    # ако обектът има run(), изпълняваме го (уязвимо)
    return obj.run() if hasattr(obj, "run") else obj
