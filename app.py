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


pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)


ssl._create_default_https_context = ssl._create_unverified_context

urlList = ['http://www.stats.gov.cn/tjsj/zxfb/index.html']
for i in range(1, 25):
    urlList.append('http://www.stats.gov.cn/tjsj/zxfb/index_%d.html' % i)


# re模块-----------------------------------------------------------
# 1、用于匹配标题链接的开头、结尾部分
URL_FOR_TITLE = '<li>\n\t\t\t\t\t\t<a href="'
URL_FOR_TITLE_END = r'" target="_blank" >'

# 2、用于匹配标题本身以及对应发布时间的开头、结尾部分
HEAD_FOR_TITLE = r'<font class="cont_tit03">'
HEAD_FOR_TIMES = r'<font class="cont_tit02">'
HEAD_FOR_END = '</font>'

# 3、用于匹配任意长度的任意字符或符号
ANY_TEXT = r'[\d\D\w\W\s\S\u4E00-\u9FA5 .%]*?'

# 4、正则表达式
para = re.compile(f'(?P<url>(?<={URL_FOR_TITLE}){ANY_TEXT}(?={URL_FOR_TITLE_END}))(?P<split_1>{ANY_TEXT})(?P<title>(?<={HEAD_FOR_TITLE}){ANY_TEXT}(?={HEAD_FOR_END}))(?P<split_2>{ANY_TEXT})(?P<time>(?<={HEAD_FOR_TIMES}){ANY_TEXT}(?={HEAD_FOR_END}))')


# request模块
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

cookie_jar = MozillaCookieJar('./log/Cookie1658392515.log')
cookie_jar.load(ignore_discard=True, ignore_expires=True)

cookie_processor = HTTPCookieProcessor(cookie_jar)
opener = build_opener(cookie_processor)


data = []
for url in urlList:
    request = Request(url, headers=headers, method='GET')

    response = opener.open(request)
    html = gzip.decompress(response.read()).decode('utf8')

    title = re.finditer(para, html)
    for i in title:
        data.append(list(i.group('url', 'title', 'time')))


# cookie_jar.save('./log/Cookie'+str(int(time.time())) + '.log',
#                 ignore_discard=True, ignore_expires=True)


# 将data存储的相对地址改为绝对地址
for i in range(len(data)):
    data[i][0] = urljoin(urlList[0], data[i][0])

# 将data对象转为pandas.DataFrame对象方便输出
df = pandas.DataFrame(data=data, columns=['网址', '标题', '发布时间'])
df.to_excel('./log/output'+str(int(time.time())) + '.xlsx')

dict.update
