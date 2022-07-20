import sqlite3
import os
from typing import *


class _conn(sqlite3.Connection):
    def __init__(self, path) -> None:
        super().__init__(path)

    def __enter__(self):
        return self.cursor()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cursor().close()
        self.close()
        if exc_traceback is None:
            ...
        else:
            ...


CHROME_COOKIE_PATH = r'\Google\Chrome\User Data\Default\network\Cookies'
CHROME_LOCALSTATE_PATH = r'\Google\Chrome\User Data\Local State'

path = os.environ['LOCALAPPDATA']
dbCookies = path + CHROME_COOKIE_PATH  # cookie文件，本质是一个sqlite数据库
fileLocalState = path + CHROME_LOCALSTATE_PATH  # 存储密钥的文件，本质是一个Json文件


with _conn(dbCookies) as cur:
    sql = """select creation_utc,host_key,name,encrypted_value,path from cookies where host_key like '%baidu%'"""
    cur.execute(sql)
    valCookies = cur.fetchall()
