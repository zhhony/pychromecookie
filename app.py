from urllib.parse import *
from urllib.request import *
from http.cookiejar import *
import time
import ssl
import gzip
import os
import re

ssl._create_default_https_context = ssl._create_unverified_context

urlList = ['http://www.stats.gov.cn/tjsj/zxfb/index.html']
for i in range(1, 25):
    urlList.append('http://www.stats.gov.cn/tjsj/zxfb/index_%d.html' % i)


# re模块资源

HEAD_1 = r'<font class="cont_tit03">'
HEAD_2 = r'<font class="cont_tit02">'
END = '</font>'

# paraTitle = re.compile(r'(?<=<font class="cont_tit03">)[\d\D\w\W\s\S\u4E00-\u9FA5 .%]*?(?=</font>)' )
# paraTime = re.compile(r'(?<=<font class="cont_tit02">)[\d\D\w\W\s\S\u4E00-\u9FA5 .%]*?(?=</font>)' )

paraTitle = re.compile(f'(?<={HEAD_1})[\d\D\w\W\s\S\u4E00-\u9FA5 .%]*?(?={END})')
paraTime = re.compile(f'(?<={HEAD_2})[\d\D\w\W\s\S\u4E00-\u9FA5 .%]*?(?={END})')


headers={
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

cookie_jar=MozillaCookieJar('./log/Cookie1658392515.log')
cookie_jar.load(ignore_discard=True, ignore_expires=True)

cookie_processor=HTTPCookieProcessor(cookie_jar)
opener=build_opener(cookie_processor)


data=[]
for url in urlList:
    request=Request(url, headers=headers, method='GET')

    response=opener.open(request)
    html=gzip.decompress(response.read()).decode('utf8')
    title=re.findall(paraTitle, html)
    data.append(title)

cookie_jar.save('./log/Cookie'+str(int(time.time())) + '.log',
                ignore_discard=True, ignore_expires=True)
