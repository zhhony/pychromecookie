from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def decode(bytes: bytes, key: str) -> str:

    # 根据百度的结果，valEncrypted的构成分为三部分，都是固定长度
    nonce = bytes[3:15]
    cipherbytes = bytes[15:]

    aesgcm = AESGCM(key)
    plainbytes = aesgcm.decrypt(nonce, cipherbytes, None)

    return plainbytes.decode('utf-8')
