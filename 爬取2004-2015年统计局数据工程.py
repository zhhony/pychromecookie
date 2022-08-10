import urllib.parse
import urllib.request
import ssl
import bs4
from modules import *
import re
import pandas


# 开启表单提取
ssl._create_default_https_context = ssl._create_unverified_context
# 定义headers
headers = {'Cache-Control': 'no-cache',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
# 定义需要查询的年份
choiceYear = []
for i in range(2005, 2015):
    choiceYear.append(f'{i}年')
# 设置等宽
pandas.set_option('display.unicode.east_asian_width', True)

# 建立request
url = r'http://www.stats.gov.cn/tjsj/ndsj/'
req = urllib.request.Request(url=url, headers=headers, method="GET")
respon = urllib.request.urlopen(req)
html = respon.read().decode('utf8')

# 解析存储了年份和网址对应关系的网页部分
soul = bs4.BeautifulSoup(html, features='lxml')
urlList = soul.find_all('td', align="center", valign="middle")

# 获取年份和网页的对应关系，存入字典{年：网址}，并转为pandas对象
urlDict = {}
for i in urlList:
    if i.a.string in choiceYear:
        urlDict[i.a.string] = i.a["href"]
dfUrl = pandas.DataFrame.from_dict(
    data=urlDict, orient="index", columns=['网址'])


for index in dfUrl.index:
    # 改造value以获取网页框架内，左边框对应的值
    subValue = urllib.parse.urljoin(dfUrl.loc[index, '网址'], 'left.htm')

    # 对value进行访问并解析内容
    subReq = urllib.request.Request(
        url=subValue, headers=headers, method="GET")
    subRespon = urlopen(subReq)
    subHtml = subRespon.read().decode('gbk')

    # 提取解析内容中存储于li标签的财政支出信息
    subSoul = bs4.BeautifulSoup(subHtml, features='lxml')
    pattern = re.compile('[^和]个体就业人数( *)\(')
    subString = subSoul.find_all(name='a', string=pattern)[0].string

    # 提取网址
    subHref = subSoul.find_all(name='a', string=pattern)[0]["href"]

    # 将网址资源的后缀从.htm改成.xls
    subHref = subHref.replace('.htm', '.xls')

    dfUrl.loc[index, '标签'] = subString
    dfUrl.loc[index, '文件位置'] = urllib.parse.urljoin(
        dfUrl.loc[index, '网址'], subHref)


# 定义存储文件的位置
path = './out/'
for index in dfUrl.index:
    Downunit(url=dfUrl.loc[index, '文件位置'],
             path=path + index + '.xls', threadnum=3).Download()


# dfUrl.loc['2014年','网址']
