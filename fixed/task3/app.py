import os

def compress(pattern,out='out.tar.gz'):
    cmd="tar -czf %s %s"%(out,pattern)
    return os.system(cmd)
