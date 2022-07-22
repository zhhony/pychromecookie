from urllib.parse import *
from urllib.request import *
from http.cookiejar import *
import time
import ssl
import gzip
import os
import re
import pandas
from bs4 import *
from py_test_tools import *
import jieba
import jieba.analyse as analyse
from zhon.hanzi import punctuation

CHROME_COOKIE_PATH = r'\Google\Chrome\User Data\Default\network\Cookies'
CHROME_LOCALSTATE_PATH = r'\Google\Chrome\User Data\Local State'

url = 'http://www.stats.gov.cn/tjsj/zxfb/202207/t20220715_1886607.html'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie': 'SF_cookie_1=37059734; _trs_uv=l5ur54wg_6_de0; _trs_ua_s_1=l5ur54wg_6_bthk',
    'Host': 'www.stats.gov.cn',
    'Pragma': 'no-cache',
    'Proxy-Authorization': 'Basic MTY1ODkzNzYwMEAyNDQ3NzMwOmUwMWQ4ZmNjZjA4ZTQxMDU0OWU0MjQxZDQ3ZmU4YTg0',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.stats.gov.cn/tjsj/zxfb/index_1.html',
    'Upgrade-Insecure-Requests': 1,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

}


request = Request(url=url, headers=headers, method='GET')

html = gzip.decompress(urlopen(request).read()).decode('utf8')


soup = BeautifulSoup(html, 'lxml')
pycls()
with open('123.html', 'w') as f:
    print(soup.p.parent, file=f)

txt = ''.join([i for i in soup.p.parent.strings])
txt = txt[txt.find('附件'):]


with open('123.html', 'w') as f:
    print(txt, file=f)

replaceList = ['\n', '\r', '\xa0', '/']
[replaceList.append(i) for i in punctuation]
for i in replaceList:
    txt = txt.replace(i, '')

wordList = jieba.lcut(txt)


wordDict = dict()
for word in wordList:
    wordDict.update({word: wordDict.setdefault(word, 0)+1})


wordDictList = [(key, value) for (key, value) in wordDict.items()]
wordDictList.sort(key=lambda x: x[1],reverse=True)
wordDict =dict(wordDictList)

df = pandas.DataFrame(data=wordDict,index=['数值'])
df.to_excel('123.xlsx')
df = df.transpose().reset_index()
df.columns = ['名词','数值']

keyword = analyse.extract_tags(txt, topK=10, withWeight=True)
keyword
