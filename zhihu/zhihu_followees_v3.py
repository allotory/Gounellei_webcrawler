# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup
import json

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

    # 查询所有关注我的人
    # data-init="{"params": {"offset": 0, "order_by": "created", "hash_id": "12010d7eaa2aad61931b26e1b17e3caa"}, "nodename": "ProfileFolloweesListV2"}"
    # 获取 hash_id
    followees_content = session.get('https://www.zhihu.com/people/elleryzhang/followees').content
    followees_soup = BeautifulSoup(followees_content, 'html.parser')
    info_div = followees_soup.find('div', attrs={'class': 'zh-general-list clearfix'})['data-init']

    data_dict = json.loads(info_div)
    hash_id = data_dict['params']['hash_id']
    params = {
        "offset": 0,
        "order_by": "created",
        "hash": hash_id
    }
    print(params)
    followees_data = {
        'method': "next",
        'params': json.dumps(params),
        '_xsrf': _xsrf
    }
    print(followees_data)
    followees_headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,id;q=0.4,ja;q=0.2,ru;q=0.2,zh-TW;q=0.2,fr;q=0.2,es;q=0.2,de;q=0.2,pt;q=0.2',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.zhihu.com',
        'referer': 'https://www.zhihu.com/people/elleryzhang/followees',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    resp = session.post('https://www.zhihu.com/node/ProfileFolloweesListV2', data=followees_data, headers=followees_headers)
    print(resp.content.decode('utf-8'))

def main() :
    login('allotory@gmail.com', 'xxxxx', kill_captcha)

if __name__ == '__main__' :
    main()