from urllib.parse import *
from urllib.request import *
from http.cookiejar import *
import time
import ssl
import gzip

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://i.csdn.net/#/user-center/profile?spm=1000.2115.3001.5111'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'uuid_tt_dd=10_18805182430-1653184353712-895197; UN=weixin_41936572; p_uid=U010000; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_18805182430-1653184353712-895197!5744*1*weixin_41936572; _ga=GA1.2.247901835.1654868387; c_adb=1; _bl_uid=26lX659ts7567dp5k5Is0aOiF2qe; UserName=weixin_41936572; UserInfo=9aecc2f43bee4d2b9c19f3a3317c292b; UserToken=9aecc2f43bee4d2b9c19f3a3317c292b; UserNick=%E5%A4%A7%E5%B0%BE%E5%B7%B4%E9%B1%BC_root; AU=825; BT=1658235715639; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_41936572%22%2C%22scope%22%3A1%7D%7D; ssxmod_itna=YuDt7KAKY5YI+Dl4iTd9D9mG30==veLUU+dD/8b+DnqD=GFDK40EYBE4D7+Kn5bALivTxNCEwt+d0Adab+MFCRoXaDU4i8DCM0Gd7+DYY8Dt4DTD34DYDixibkxi5GRD0KDFF5XUZ9Dm4GW9qDgR4GgDCiD0+Uc3wiD4qDBCodDKM0cDGAjYmUdpMG=kAhcD0UqxBLeWavcICcFcrX=56nDNEQDzkHDtut5wMbDC2=/Ud0zIBmxIY4zQY+ebgG5F741tDwvuDxGWGMYt7he44wQfB4AHH5DGfx1jYjKeD===; ssxmod_itna2=YuDt7KAKY5YI+Dl4iTd9D9mG30==veLUU4G9QkIIDBqqLq7pwwIBKb7FkD7+d7=YINGTKKqqLq2e4Q2rG7GflB4FP7KLucwoHbCvN07xXYKGFjaCSRnV9cPtBzY2oHk0wNGkuM=l4onFN6mT2ln8b6K+jYuD/meFq7maNE4z=BuxGOWKX1gxRDmmKxmQzIWq970k13m3j7Os0oWbc+ed8+LN=pHhgtukS4n0DVLUoDlTF2L0xTCFikw1/B9ePmCcuf6uUpx0UpWcZttzCuQ8fxz6GsQ8UsIAGLBS1VmBArsc0HSl1qsXCuO7y/zwDx7yWHgG9OiY/8BVSFVf9erTV8wWRWztwW9+=BYU/7IQH/mAoxR5p2qoHSSFDP4rQxDKuxHdQ8xqL+K2AIAnK1YvQOvtBI174bhKPfqh85VlAu7vS7mPDqcSDX+5l03fS5aPoHadlDDLxD2BhDD=; c_dl_prid=-; c_dl_rid=1658243467166_372809; c_dl_fref=https://blog.csdn.net/weixin_39975366/article/details/111068878; c_dl_fpage=/download/goodnet520/10434809; c_dl_um=distribute.pc_relevant_t0.none-task-blog-2%7Edefault%7EOPENSEARCH%7Edefault-1-111068878-blog-125874336.pc_relevant_multi_platform_whitelistv1_exp2; management_ques=1658244200670; dc_session_id=10_1658325354140.745621; c_segment=13; dc_sid=587c626fd333d0750b9f6a05f3038d45; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1657977274,1658020329,1658235582,1658325355; c_hasSub=true; c_pref=default; log_Id_click=137; c_ref=https%3A//www.baidu.com/link; c_first_ref=www.baidu.com; c_first_page=https%3A//blog.csdn.net/a807557328/article/details/99677230; c_dsid=11_1658327637145.571618; c_page_id=default; dc_tos=rfbpsl; log_Id_pv=153; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1658327637; log_Id_view=312',
    'pragma': 'no-cache',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': 1,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

cookie_jar = MozillaCookieJar('./log/Cookie1658325641.log')
cookie_jar.load(ignore_discard=True, ignore_expires=True)

cookie_processor = HTTPCookieProcessor(cookie_jar)
opener = build_opener(cookie_processor)



request = Request(url, headers=headers, method='GET')

response = opener.open(request)
data = response.read()

print(gzip.decompress(data).decode('utf-8'))

cookie_jar.save('./log/Cookie'+str(int(time.time())) + '.log',
                ignore_discard=True, ignore_expires=True)
