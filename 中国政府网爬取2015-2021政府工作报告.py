import ssl
import pandas
import pathlib
from zhon import pinyin
from http.cookiejar import *
from urllib.parse import *
from urllib.request import *
from bs4 import *


# 常用参数设置
pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)
ssl._create_default_https_context = ssl._create_unverified_context

# 一、获取网页内容
urlList = []
for year in range(2015, 2022):
    urlList.append(f'http://www.gov.cn/guowuyuan/{year}zfgzbg.htm')

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Cookie': 'wdcid=19c0cc947b9d60c7; __auc=dca5428718225331278a9fb15c5; allmobilize=mobile; wdses=1ff826d6dab4248d; __asc=a1768f9d1823486103e4d33f5cf; wdlast=1658739342',
    'Host': 'www.gov.cn',
    'Pragma': 'no-cache',
    'Proxy-Authorization': 'Basic MTY1OTI4MzIwMEAyNDQ3NzMwOjQ2ZTRlYWM1MGEzNDllZGZkNDVjN2M1YTM0YWRmZWU4',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://www.gov.cn/guowuyuan/2014zfgzbg.htm',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

for url in urlList:
    request = Request(url=url, headers=headers, method='GET')

    response = urlopen(request)
    html = response.read().decode('utf8')
    soul = BeautifulSoup(html)

    title = soul.find_all('title')[0].string
    title = title.replace('\t','')
    title = title.replace('\n','')
    title = title.replace('\r','')

    div = soul.find_all('div', class_="conlun2_box_text",
                        id="conlun2_box_text")
    file = [i.get_text() for i in div][0]
    with open('./out/' + title + '.txt', 'w') as f:
        f.write(file)
