import importlib.util
import pathlib

# Compute repo root reliably (parent of tests/ directory)
THIS = pathlib.Path(__file__).resolve()
TESTS_DIR = THIS.parent
REPO_ROOT = TESTS_DIR.parent

def _resolve_path(p):
    p = pathlib.Path(p)
    # If it's absolute or already under repo root, return resolved
    if p.is_absolute():
        return p
    # If the relative path already points to an existing file from cwd, keep it.
    alt = (pathlib.Path.cwd() / p)
    if alt.exists():
        return alt.resolve()
    # Otherwise resolve relative to repository root (most robust for test runner)
    candidate = (REPO_ROOT / p).resolve()
    return candidate

def load_module_from_path(path, mod_name=None):
    """
    Load a module from a file path and return the module object.
    'path' may be absolute or relative; relative paths are resolved
    against the repo root (preferred) or cwd if that file exists.
    """
    p = _resolve_path(path)
    if not p.exists():
        raise FileNotFoundError(f"Module path not found: {p}")
    if mod_name is None:
        # create unique module name from absolute path
        mod_name = "mod_" + p.as_posix().replace("/", "_").replace(":", "_").replace(".", "_")
    spec = importlib.util.spec_from_file_location(mod_name, str(p))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
