from urllib.parse import *
from urllib.request import *
from http.cookiejar import *
import time
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

url = 'https://i.csdn.net/#/user-center/profile?spm=1000.2115.3001.5111'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

cookie_jar = MozillaCookieJar('./log/Cookie1658309064.log')
cookie_jar.load(ignore_discard=True, ignore_expires=True)

cookie_processor = HTTPCookieProcessor(cookie_jar)
opener = build_opener(cookie_processor)

request = Request(url, headers=headers, method="GET")

response = opener.open(request)
data = response.read().decode('utf8')

print(data)

cookie_jar.save('./log/Cookie'+str(int(time.time())) + '.log',
                ignore_discard=True, ignore_expires=True)
