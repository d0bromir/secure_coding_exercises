import logging, tempfile
from pathlib import Path

def _log_path(filename):
    base = Path(tempfile.gettempdir()); base.mkdir(parents=True, exist_ok=True)
    return str(base/filename)
logger = logging.getLogger('vuln8')
if not logger.handlers:
    logger.addHandler(logging.FileHandler(_log_path('vuln8.log'), encoding='utf-8'))
    logger.setLevel(logging.INFO)

def process_login(username,password):
    logger.info('login attempt: username=%s password=%s', username, password)
    return username=='alice' and password=='alicepass'
