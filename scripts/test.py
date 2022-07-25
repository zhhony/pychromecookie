from urllib.parse import *
from urllib.request import *
from http.cookiejar import *
import gzip
import pandas
from bs4 import *
import jieba
import jieba.analyse as analyse
from zhon.hanzi import punctuation
from yonghong.script.port import EntryPoint,ResourceType
from datetime import datetime

pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)


url = 'http://www.bailuzhiku.com/policy/detail/20200206115111584001208029P.html'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_ec196724ce16461e3c277405b7fd5b34=1658482091; ASP.NET_SessionId=3pyrn5ntul4cumh42thggtf4; login=3BD60B3CD39B6D9F8B661DD868A38B932A2A780B235B752568104D958FB23240B12428E9870CD2A52D05BBFBDF18A4C6500B474E7D50DDEAF92BEA82FFDB91F61D9A8F0D43376705EA1FCBF5507ED8A0A8FF69BF6D1E7F280F430A628C465CEFF35E7AB4987E3A1BF611C4F4FEDD68DEFB73B074B67077B43E3161BC9F01055FB25A6FF037CEDF337E190CC3715A6DE12B580F27; Hm_lpvt_ec196724ce16461e3c277405b7fd5b34=1658482120',
    'Host': 'www.bailuzhiku.com',
    'Pragma': 'no-cache',
    'Pragma': 'no-cache',
    'Proxy-Authorization': 'Basic MTY1OTAyNDAwMEAyNDQ3NzMwOmIxMjFkMzJmNGNkNWQ5MmZlMmRhNTdmOWUzYjIwNzFk',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'https://www.baidu.com/link?url=Hl-dUTBa05BeuU5wnLyu4SBNkCBPimELTUpjjP9F0ixW27SEUxremKVHYfAjwt0xa5SyXjra4tJsqFR_qjRL_MS3612ZR8LRgaX6R5Iu0ylwfK-G_4poIY6PmE1wmlwi&wd=&eqid=85d8c9d0000612840000000462da6cb2',
    'Upgrade-Insecure-Requests': 1,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

}


cookie_jar = MozillaCookieJar(r'C:\Users\zhhony\Desktop\Cookie1658482201.log')
cookie_jar.load(ignore_discard=True, ignore_expires=True)

cookie_processor = HTTPCookieProcessor(cookie_jar)
opener = build_opener(cookie_processor)

request = Request(url=url, headers=headers)
response = opener.open(request)

# html = gzip.decompress(urlopen(response).read()).decode('utf8')
html = response.read().decode('utf8')


soup = BeautifulSoup(html, 'lxml')

txt = ''.join([i for i in soup.p.parent.strings])
# txt = txt[txt.find('附件'):]


replaceList = ['\n', '\r', '\xa0', '/','和','的','0','1','2','3','4','5','6','7','8','9']
[replaceList.append(i) for i in punctuation]
for i in replaceList:
    txt = txt.replace(i, '')

wordList = jieba.lcut(txt)


wordDict = dict()
for word in wordList:
    wordDict.update({word: wordDict.setdefault(word, 0)+1})


wordDictList = [(key, value) for (key, value) in wordDict.items()]
wordDictList.sort(key=lambda x: x[1],reverse=True)
wordDict =dict([i for i in wordDictList if i[1]>4])

df = pandas.DataFrame(data=wordDict,index=['数值'])
df = df.transpose().reset_index()
df.columns = ['名词','数值']


entry = EntryPoint()
entry.output.dataset = df
