# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup
import json
import re

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

    return _xsrf, session

def get_following_count(session) :
    resp = session.get('https://www.zhihu.com/question/following').content
    soup = BeautifulSoup(resp, 'html.parser')
    following_count = soup.find('span', attrs={'class': 'zg-gray-normal'}).string
    m = re.match(r'^\（(\d+)\）$', following_count)
    return m.group(1)


def followed_question(_xsrf, session, offset) :
    # 查询所有我关注的问题
    # 获取 hash_id
    params = {
        'offset': offset
    }
    following_data = {
        'method': 'next',
        'params': json.dumps(params),
        '_xsrf': _xsrf
    }
    following_headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,id;q=0.4,ja;q=0.2,ru;q=0.2,zh-TW;q=0.2,fr;q=0.2,es;q=0.2,de;q=0.2,pt;q=0.2',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.zhihu.com',
        'referer': 'https://www.zhihu.com/question/following',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    resp = session.post('https://www.zhihu.com/node/ProfileFollowedQuestionsV2', data=following_data, headers=following_headers)
    json_data = json.loads(resp.content.decode('utf-8'))
    
    return json_data

def parse_html(html) :
    soup = BeautifulSoup(html, 'html.parser')
    # vote_num = soup.find('div', attrs={'class': 'zm-profile-vote-num'}).getText()
    question = soup.find('a', attrs={'class': 'question_link'}).getText()
    # print(vote_num)
    print(question)


def main() :
    _xsrf, session = login('allotory@gmail.com', 'xxxxx', kill_captcha)
    following_count = int(get_following_count(session))
    offset = 0
    while offset < following_count :
        json_data = followed_question(_xsrf, session, offset)
        counter = 20
        if following_count - offset < 20 :
            counter = following_count - offset

        for i in range(counter) :
            # print(json_data['msg'][i])
            parse_html(json_data['msg'][i])

        offset += 20

if __name__ == '__main__' :
    main()