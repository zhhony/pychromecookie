import ssl
import pandas
import pathlib
from http.cookiejar import *
from urllib.parse import *
from urllib.request import *
from bs4 import *

from modules.download import *


# 常用参数设置
pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)
ssl._create_default_https_context = ssl._create_unverified_context


# 一、获取网页内容
url = 'http://www.bailuzhiku.com/hot/detail/590ccc0d846e4308a4842ae18208730c.html'

# 1、载入cookie文件
cookieJar = MozillaCookieJar('./log/Cookie1658712908.log')
cookieJar.load(ignore_discard=True, ignore_expires=True)

# 2、获取OpenerDirector对象
cookieProcess = HTTPCookieProcessor(cookieJar)
opener = build_opener(cookieProcess)

# 3、定义headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_ec196724ce16461e3c277405b7fd5b34=1658482091,1658712326; ASP.NET_SessionId=2exrtxywj12rzk3dxbwq3bfo; login=8C4D79421C5D0C3493C1EC67307768593F285D798DEBB45B72966AF63F0E2F1CE9ED8809C8C0860597668EA6967CE519CEA68BB23F890F9BD4573CAE0B09D6EB0D5086D7496817AF2670AD87F083BD1AEDFC892A5959E4BFE9394887DED9E4EF3741D3116EB2CD46239F67BF2CEAAA2750CA3E641CBA8C81985874D8F35E2C6B396E5374C69087FC959BE37D58056C3288EBD8D8; Hm_lpvt_ec196724ce16461e3c277405b7fd5b34=1658718592',
    'Host': 'www.bailuzhiku.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.baidu.com/link?url=Hl-dUTBa05BeuU5wnLyu4SBNkCBPimELTUpjjP9F0ixW27SEUxremKVHYfAjwt0xa5SyXjra4tJsqFR_qjRL_MS3612ZR8LRgaX6R5Iu0ylwfK-G_4poIY6PmE1wmlwi&wd=&eqid=85d8c9d0000612840000000462da6cb2',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


# 4、定义request对象
request = Request(url=url, headers=headers, method='GET')

# 5、获取html
response = opener.open(request)
html = response.read().decode('utf8')

soup = BeautifulSoup(html, 'lxml')

# 二、数据清洗，获取历年报告字典（url:title）
htmlBox_A = [i for i in soup.find_all('a', class_='link', target='_blank')]
htmlBox_A = [(urljoin(url, i.get('href')), i.string) for i in htmlBox_A]

reportUrlDict = dict(htmlBox_A)

# 三、针对每一张网页获取报告正文的_UrlopenRet对象
headers['Referer'] = 'http://www.bailuzhiku.com/hot/detail/590ccc0d846e4308a4842ae18208730c.html'

reportList = []
for reportUrl, reportTitle in list(reportUrlDict.items()):
    reportrequest = Request(url=reportUrl, headers=headers, method="GET")
    reportresponse = opener.open(reportrequest)
    reportList.append((reportresponse, reportTitle))

# PS:一个账户只有50次进入报告详览的机会,所以先将文件保存下来以备后用
for response, title in reportList:
    reportHtml = response.read().decode('utf8')
    with open('./out/' + str(title) + '.log', 'w') as f:
        f.write(reportHtml)

outPath = pathlib.Path('./out')
outPathFile = [i for i in outPath.glob('**/*.log')]

for file in outPathFile:
    with open(file, 'r') as f:
        reportSoup = BeautifulSoup(f, 'lxml')
        if reportSoup.find_all('a', style=True, target=False) == []:
            with open(str(file)+'.txt', 'w') as e:
                [e.write(str(j.string)+'\n')
                 for j in reportSoup.find_all('p', style=True)]
        else:
            downloadUrl = reportSoup.find_all(
                'a', style=True, target=False)[0].get('href')
            Downunit(downloadUrl, str(file)+'.pdf').Download()
