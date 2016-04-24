# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def login(username, password) :

    s = requests.session()

    # 获取 once 字段
    signin_content = s.get('https://www.v2ex.com/signin').content
    soup = BeautifulSoup(signin_content, 'html.parser')
    once = soup.find('input', attrs={'type': 'hidden', 'name': 'once'})['value']

    # 获取用户名、密码两个字段的名称
    form_data_name = soup.find_all('input', attrs={'class': 'sl'})
    u = form_data_name[0].attrs['name']
    p = form_data_name[1].attrs['name']

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,id;q=0.4,ja;q=0.2,ru;q=0.2,zh-TW;q=0.2,fr;q=0.2,es;q=0.2,de;q=0.2,pt;q=0.2',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.v2ex.com',
        'referer': 'https://www.v2ex.com/signin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
    }

    data = {
        u: username,
        p: password,
        'once': once,
        'next': '/'
    }

    # 登陆
    s.post('https://www.v2ex.com/signin', headers=headers, data=data)

    # 访问 setting 页面
    settings_content = s.get('http://www.v2ex.com/settings', headers=headers).content
    print(settings_content)

def main() :
    login('allotory', 'xxxxx')

if __name__ == '__main__' :
    main()