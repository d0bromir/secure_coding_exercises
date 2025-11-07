import os

def write_if_safe(path,content):
    if os.path.islink(path):
        raise RuntimeError('symlink')
    open(path,'w').write(content)
