from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

K=b'0123456789abcdef'

def encrypt(pt:bytes,aad=b''):
    return None, None, AES.new(K,AES.MODE_ECB).encrypt(pad(pt,16))

def decrypt(key,nonce,ct,aad=b''):
    from Crypto.Util.Padding import unpad
    return unpad(AES.new(K,AES.MODE_ECB).decrypt(ct),16)
