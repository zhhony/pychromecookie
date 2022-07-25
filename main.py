from modules import *
import os


# 存储cookie、密钥的文件路径
CHROME_COOKIE_PATH = r'\Google\Chrome\User Data\Default\network\Cookies'
CHROME_LOCALSTATE_PATH = r'\Google\Chrome\User Data\Local State'

path = os.environ['LOCALAPPDATA']
dbCookies = path + CHROME_COOKIE_PATH  # cookie文件，本质是一个SQlite数据库
fileLocalState = path + CHROME_LOCALSTATE_PATH  # 存储密钥的文件，本质是一个Json文件

KEY_WORD = r'%bailuzhiku%'

with Conn(dbCookies) as cur:
    sql = """select creation_utc,host_key,name,encrypted_value,path from cookies where host_key like '%s'""" % KEY_WORD
    cur.execute(sql)
    valCookiesWithEncode = cur.fetchall()

valCookiesWithDecode = []

# 从Local State文件里获取key
key = DecodeKey(fileLocalState)

for i in valCookiesWithEncode:
    creation_utc, host_key, name, valEncrypted, path = i

    value = DecodeValue(valEncrypted, key)
    valCookiesWithDecode.append(
        tuple((creation_utc, host_key, name, value, path)))

cookies = Cookie(valCookiesWithDecode)
cookies.getOutFile()
