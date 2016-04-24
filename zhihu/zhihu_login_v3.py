# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup

def kill_captcha(data) :
    with open('captcha.png', 'wb') as f :
        f.write(data)
    return input('captcha:')

def login(username, password, oncaptcha) :
    session = requests.session()

    # 获取登录页面的xsrf
    login_content = session.get('https://www.zhihu.com/#signin').content
    soup = BeautifulSoup(login_content, 'html.parser')
    _xsrf = soup.find('input', attrs={'name': '_xsrf'})['value']

    # 得到验证码内容
    unix_time = time.time() * 1000
    captcha_content = session.get('http://www.zhihu.com/captcha.gif?r=%d&type=login' % unix_time).content
    captcha_text = oncaptcha(captcha_content)

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,id;q=0.4,ja;q=0.2,ru;q=0.2,zh-TW;q=0.2,fr;q=0.2,es;q=0.2,de;q=0.2,pt;q=0.2',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': 'https://www.zhihu.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
    }

    data = {
        '_xsrf': _xsrf,
        'password': password,
        'captcha': captcha_text,
        'remember_me': 'true',
        'email': username
    }

    # 登录
    resp = session.post('https://www.zhihu.com/login/email', data, headers).content
    print(resp.decode('unicode_escape'))

def main() :
    login('allotory@msn.com', 'xxxxx', kill_captcha)

if __name__ == '__main__' :
    main()