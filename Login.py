import urllib.error
import urllib.request
import re
import rsa
import http.cookiejar
import base64
import json
import urllib
import urllib.parse
import binascii


class Login:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def prelogin_args(self):
        json_pattern = re.compile('\((.*)\)')
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&' + self.encrypted_name() + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            raw_data = response.read().decode('utf-8')
            json_data = json_pattern.search(raw_data).group(1)
            data = json.loads(json_data)
            return data
        except urllib.error.URLError as err:
            print('urllib error:' + str(err))
            return None

    def encrypted_pw(self, data):
        rsa_e = 65537 #0x10001
        pw_string = str(data['servertime']) + '\t' + str(data['nonce']) + '\n' + str(self.password)
        key = rsa.PublicKey(int(data['pubkey'], 16), rsa_e)
        pw_encypted = rsa.encrypt(pw_string.encode('utf-8'), key)
        self.password = ''
        passwd = binascii.b2a_hex(pw_encypted)
        #print(passwd)
        return passwd

    def encrypted_name(self):
        username_urllike= urllib.request.quote(self.username)
        username_encrypted = base64.b64encode(bytes(username_urllike, encoding='utf-8'))
        return username_encrypted.decode('utf-8')

    def enableCookies(self):
            cookie_container = http.cookiejar.CookieJar()
            #将一个cookies容器和一个HTTP的cookie的处理器绑定
            cookie_support = urllib.request.HTTPCookieProcessor(cookie_container)
            #创建一个opener,设置一个handler用于处理http的url打开
            opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
            #安装opener，此后调用urlopen()时会使用安装过的opener对象
            urllib.request.install_opener(opener)

    def build_post_data(self, raw):  
        post_data = {
            "entry":"weibo",
            "gateway":"1",
            "from":"",
            "savestate":"0",
            "useticket":"1",
            "pagerefer": "",
            "vsnf":"1",
            "su":self.encrypted_name(),
            "service":"miniblog",
            "servertime":raw['servertime'],
            "nonce":raw['nonce'],
            "pwencode":"rsa2",
            "rsakv":raw['rsakv'],
            "sp":self.encrypted_pw(raw),
            "sr":"1280*800",
            "encoding":"UTF-8",
            "prelt":"77",
            "url":"http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype":"META"
        }
        data = urllib.parse.urlencode(post_data).encode('utf-8')
        #print(data)
        return data

    def login(self):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        self.enableCookies()
        data = self.prelogin_args()
        post_data = self.build_post_data(data)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        }
        try:
            request = urllib.request.Request(url=url, data=post_data, headers=headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('GBK')
           # print(html)

        except urllib.error as e:
            print(e.code)

        p = re.compile('location\.replace\(\'(.*?)\'\)')
        p2 = re.compile(r'"userdomain":"(.*?)"')

        try:
            login_url = p.search(html).group(1)
           # print(login_url)
            request = urllib.request.Request(login_url)
            response = urllib.request.urlopen(request)
            page = response.read().decode('utf-8')
            #print(page)

            login_url = 'http://weibo.com/' + p2.search(page).group(1)
            request = urllib.request.Request(login_url)
            response = urllib.request.urlopen(request)
            final = response.read().decode('utf-8')
            #print(final)

            print("Login success!")
        except:
            print('Login error!')
            return 0

'''
user = Login('#usrname', '#pswd')
user.login()

url = 'http://weibo.com/p/1001018008631000000000000'

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
raw = response.read().decode()

print(raw)
'''