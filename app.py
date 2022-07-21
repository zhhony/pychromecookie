from urllib.parse import *
from urllib.request import *
from http.cookiejar import *
import time
import ssl
import gzip
import re

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://blog.csdn.net/weixin_41936572?spm=1000.2115.3001.5343'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'uuid_tt_dd=10_20454972790-1658310927841-120288; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_20454972790-1658310927841-120288!5744*1*weixin_41936572; c_adb=1; hide_login=1; UserName=weixin_41936572; UserInfo=f9c034bcc64743b1bfb20704d6fca8ca; UserToken=f9c034bcc64743b1bfb20704d6fca8ca; UserNick=%E5%A4%A7%E5%B0%BE%E5%B7%B4%E9%B1%BC_root; AU=825; UN=weixin_41936572; BT=1658310938922; p_uid=U010000; ssxmod_itna=eqfxRiG=DQu4uDl4iuYtbeDtN5YvvtGkQUecUDBLY4iNDnD8x7YDv++vnF+QFiFArW34iUB2yfGdFhmoAhQw=0OeoDU4i8DCMrEorDeW=D5xGoDPxDeDADYE6DAqiOD7qDdfhTXtkDbxi3fxDbDim8mxGCDeKD0ZbFDQKDuEF4NjG8PIa+uPOCNWBDqAKD9=oDsrDfO97fLUizPKSADI4ODlKUDCF1uEyFr4Gd66v1D9ueE7D7l7D3ejb58B2eimD7KicqTAGNblG5eWW47W2Pr0wPdDDWt7r4riGDD=; ssxmod_itna2=eqfxRiG=DQu4uDl4iuYtbeDtN5YvvtGkQUecD8qZiqGX42oGaIFeprQCx8Oi9gvAFdmrYBL+VbGnGRFuDtiANAdk/0g=jqCOGANE6lYLvux=MZ1O4Rr1gLy=U60UuD74nokAoIFAsBdhY3=vYnLwYQfpYefxouA09OI1mTAR3uNQMMrM/2whYkLlWn09momiZWbB9RpbdYWsQYa+BQnkoRrO=aqCYpIsQYWAIYWsvkbOi9B104dX8EbOmdX1KkQ=Ow6m5qOLNT7vjuF0UCG69Z8f5v6YXlKABOj/F880j5dxp95cmUU6CowjqU1ESWiE=IzGNE2IM1t4OEVofwGoK+E6mNRYN/hK67XkBjsnQ3ZtEhIS2XTg5+ie=l3Olp50L5GDa+PzQqUONGm=x3w19r2pjxYX9xn2gdmZTcOemONAjXRGi+mrafUI7bHIYWOf1OLwDPW6DHjppE5uZeCBeA1m/Ce0GwomGxG4DQF5iydWuqlpxbGFKGzPjbSdtDlNG0z5gez9ql94KKhd8wrcwV2GpOKA2ITi5zx7z0IvLr+xDFqD+6GhnHrQPbpv+3D=; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_41936572%22%2C%22scope%22%3A1%7D%7D; c_hasSub=true; dc_session_id=10_1658365812538.636101; c_first_ref=default; c_first_page=https%3A//www.csdn.net/; c_segment=0; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1658214385,1658279357,1658310930,1658365815; dc_sid=03ea6ac265b1dfc72bb9fe6f3632946d; has-vote-msg=1; utm_source=app; c_utm_source=app; c_dsid=11_1658365863678.043004; csrfToken=2MP1a3DRDI_B3-HSbD0gf6xT; log_Id_click=14; c_pref=https%3A//blog.csdn.net/rank/list; c_ref=https%3A//blog.csdn.net/weixin_41936572%3Fspm%3D1000.2115.3001.5343; c_page_id=default; dc_tos=rfckep; log_Id_pv=21; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1658367314; log_Id_view=17',
    'pragma': 'no-cache',
    'referer':'https://blog.csdn.net/weixin_41936572?spm=1000.2115.3001.5343',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': 1,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

cookie_jar = MozillaCookieJar('./log/Cookie1658367398.log')
cookie_jar.load(ignore_discard=True, ignore_expires=True)

cookie_processor = HTTPCookieProcessor(cookie_jar)
opener = build_opener(cookie_processor)


request = Request(url, headers=headers, method='GET')
opener.addheaders = [('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')]

response = opener.open(request)
data = response.read()

with open(r"C:\Users\zhhony\Desktop\Untitled-1.html", 'wb') as f:
    f.write(gzip.decompress(data))

cookie_jar.save('./log/Cookie'+str(int(time.time())) + '.log',
                ignore_discard=True, ignore_expires=True)
