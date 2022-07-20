import json
import time
from typing import *


with open('./resource/config', 'r') as f:
    BAIDU_BOOL = json.load(f)

# cookie文件头，最后一步手工生成cookie会用得到
COOKIE_HEADER = """# Netscape HTTP Cookie File\n# http://curl.haxx.se/rfc/cookie_spec.html\n# This is a generated file!  Do not edit.\n\n"""


class Cookie:
    '''这个类可以用来生成cookie文件'''

    def __init__(self, cookieList: List[Tuple[str, str, str, str, str]]) -> None:
        self.cookieList = cookieList

    def __repr__(self) -> str:
        return 'Cookie(count=%d)' % len(self.cookieList)

    def getOne(self):
        '''将cookie封装成生成器对象，通过next()函数调用'''
        for i in self.cookieList:
            creation_utc, host_key, name, value, path = i
            cookieContent = str(host_key) + '\t' + str(BAIDU_BOOL[host_key][0] if host_key in BAIDU_BOOL.keys() else 'FALSE') + '\t' + str(path) + '\t' + str(
                BAIDU_BOOL[host_key][1] if host_key in BAIDU_BOOL.keys() else 'FALSE') + '\t' + str(creation_utc) + '\t' + str(name) + '\t' + str(value)
            yield cookieContent

    def getAll(self):
        '''将cookie所有内容输出到控制台'''
        for i in self.cookieList:
            creation_utc, host_key, name, value, path = i
            cookieContent = str(host_key) + '\t' + str(BAIDU_BOOL[host_key][0] if host_key in BAIDU_BOOL.keys() else 'FALSE') + '\t' + str(path) + '\t' + str(
                BAIDU_BOOL[host_key][1] if host_key in BAIDU_BOOL.keys() else 'FALSE') + '\t' + str(creation_utc) + '\t' + str(name) + '\t' + str(value)
            print(cookieContent)

    def getOutFile(self, path: str = './log/'):
        '''将cookie封装进文件'''
        with open(path + 'Cookie'+str(int(time.time())) + '.log', 'w') as f:
            # 写入头
            f.write(COOKIE_HEADER)

            # 写入体
            for i in self.cookieList:
                creation_utc, host_key, name, value, path = i
                cookieContent = str(host_key) + '\t' + str(BAIDU_BOOL[host_key][0] if host_key in BAIDU_BOOL.keys() else 'FALSE') + '\t' + str(path) + '\t' + str(
                    BAIDU_BOOL[host_key][1] if host_key in BAIDU_BOOL.keys() else 'FALSE') + '\t' + str(creation_utc) + '\t' + str(name) + '\t' + str(value) + '\n'
                f.write(cookieContent)
