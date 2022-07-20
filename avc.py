import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import re
import sys

class CsdnCookie:
    def __init__(self):
        self.login_url = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'        
        self.verify_url = 'https://passport.csdn.net/account/verify'        
        self.my_url = 'https://my.csdn.net/'        
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'        
        self.user_headers = {            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",            'Accept - Encoding': "gzip, deflate, br",            'Connection': "Keep-Alive",            'User-Agent': self.user_agent        }        
        self.cookie_dir = 'C:/Users/ecaoyng/Desktop/PPT/cookie_csdn.txt'    
    def get_lt_execution(self):        
        cookie = http.cookiejar.MozillaCookieJar(self.cookie_dir)        
        handler = urllib.request.HTTPCookieProcessor(cookie)        
        opener = urllib.request.build_opener(handler)        
        # request = urllib.request.Request(self.login_url, headers=self.user_headers)        
        try:            
            response = opener.open(self.login_url)            
            page_src = response.read().decode(encoding="utf-8")            
            pattern = re.compile(                'login.css;jsessionid=(.*?)".*?name="lt" value="(.*?)" />.*?name="execution" value="(.*?)" />', re.S)            
            items = re.findall(pattern, page_src)            
            print(items)            
            print('='*80)            
            values = {                'username' : "username",                'password' : "password",                'lt' : items[0][1],                'execution' : items[0][2],                '_eventId' : "submit"            }            
            post_data = urllib.parse.urlencode(values)            
            post_data = post_data.encode('utf-8')            
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')]            
            self.verify_url = self.verify_url + ';jsessionid=' + items[0][0]            
            print('=' * 80)            
            print(self.verify_url)            
            print('=' * 80)            
            response_login=opener.open(self.verify_url,post_data)            
            print(response_login.read().decode(encoding="utf-8"))            
            for i in cookie:                
                print('Name: %s' % i.name)                
                print('Value: %s' % i.value)            
                print('=' * 80)            
                cookie.save(ignore_discard=True, ignore_expires=True)            
                my_page=opener.open(self.my_url)            
                print(my_page.read().decode(encoding = 'utf-8'))        
        except urllib.error.URLError as e:            
            ... 
    def access_other_page(self):        
        try:            
            cookie = http.cookiejar.MozillaCookieJar()            
            cookie.load(self.cookie_dir, ignore_discard=True, ignore_expires=True)            
            get_request = urllib.request.Request(self.my_url, headers=self.user_headers)            
            access_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))            
            get_response = access_opener.open(get_request)            
            print('='*80)            
            print(get_response.read().decode(encoding="utf-8"))        
        except Exception as e:            
            ...
            
if __name__ == '__main__':    
    print(sys.getdefaultencoding())    
    print('='*80)    
    cookie_obj=CsdnCookie()    
    # cookie_obj.get_lt_execution()    
    cookie_obj.access_other_page()