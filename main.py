from modules.conn import Conn
from modules.decode import decode
from modules.cookie import Cookie
import os
import json
import base64
import win32crypt

# 存储cookie、密钥的文件路径
CHROME_COOKIE_PATH = r'\Google\Chrome\User Data\Default\network\Cookies'
CHROME_LOCALSTATE_PATH = r'\Google\Chrome\User Data\Local State'

path = os.environ['LOCALAPPDATA']
dbCookies = path + CHROME_COOKIE_PATH  # cookie文件，本质是一个sqlite数据库
fileLocalState = path + CHROME_LOCALSTATE_PATH  # 存储密钥的文件，本质是一个Json文件

KEY_WORD = r'%baidu%'

with Conn(dbCookies) as cur:
    sql = """select creation_utc,host_key,name,encrypted_value,path from cookies where host_key like '%s'""" % KEY_WORD
    cur.execute(sql)
    valCookiesWithEncode = cur.fetchall()

valCookiesWithDecode = []

# 从Local State文件里获取key
with open(fileLocalState, 'r', encoding='utf-8') as f:
    jsonStr = json.load(f)
    encryptedKey = jsonStr['os_crypt']['encrypted_key']
encrypted_key_with_header = base64.b64decode(encryptedKey)
encrypted_key = encrypted_key_with_header[5:]
key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

for i in valCookiesWithEncode:
    creation_utc, host_key, name, valEncrypted, path = i

    value = decode(valEncrypted, key)
    valCookiesWithDecode.append(
        tuple((creation_utc, host_key, name, value, path)))

cookies = Cookie(valCookiesWithDecode)
cookies.getOutFile()
