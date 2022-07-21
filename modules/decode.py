from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import json
import base64
import win32crypt


def DecodeKey(path: str) -> str:
    '''本函数用于将local state中封装的密钥解密出来'''
    with open(path, 'r', encoding='utf-8') as f:
        jsonStr = json.load(f)
        encryptedKey = jsonStr['os_crypt']['encrypted_key']
    encrypted_key_with_header = base64.b64decode(encryptedKey)
    encrypted_key = encrypted_key_with_header[5:]
    return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]


def DecodeValue(bytes: bytes, key: str) -> str:
    '''本函数用于将cookie中加密的value解密出来'''
    # 根据百度的结果，valEncrypted的构成分为三部分，都是固定长度
    nonce = bytes[3:15]
    cipherbytes = bytes[15:]

    aesgcm = AESGCM(key)
    plainbytes = aesgcm.decrypt(nonce, cipherbytes, None)

    return plainbytes.decode('utf-8')
