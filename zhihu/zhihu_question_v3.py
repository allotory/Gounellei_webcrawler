# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup
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

def question_info(session, question_id) :
    resp = session.get('https://www.zhihu.com/question/' + question_id).content
    soup = BeautifulSoup(resp, 'html.parser')

    # 问题标题
    title = soup.find('h2', attrs={'class': 'zm-item-title zm-editable-content'})
    print('标题：', title.string.strip())

    # 问题标签
    label = soup.find('div', attrs={'class': 'zm-tag-editor-labels zg-clear'})
    tags = label.find_all('a', attrs={'class': 'zm-item-tag'})
    print('标签：', end='')
    sp = ''
    for tag in tags:
        print(sp, end='')
        print(tag.string.strip(), end='')
        sp = '、'
    print()

    # 问题细节
    content_wrap = soup.find('div', attrs={'id': 'zh-question-detail'})
    content = content_wrap.find('div', attrs={'class': 'zm-editable-content'})
    print('问题细节：', content.string.strip())

def answers_info(session, question_id):
    resp = session.get('https://www.zhihu.com/question/' + question_id).content
    soup = BeautifulSoup(resp, 'html.parser')

    # 答案数量
    answer_count = soup.find('h3', attrs={'id': 'zh-question-answer-num'})
    print('本问题共 %s' % answer_count.string.strip())

    # 答案
    counter = 1
    answer_wraps = soup.find_all('div', attrs={'class': 'zm-item-answer'})
    if answer_wraps is None:
        print('该问题暂时还没有回答')
    else:
        for answer in answer_wraps:
            # 编号
            print('No.', counter)
            counter += 1

            # 赞同数
            vote_up = answer.find('span', attrs={'class': 'count'})
            print('获得赞同：', vote_up.string)

            # 作者
            author = answer.find('a', attrs={'class': 'author-link'})
            print('作者：', author.string)

            # 答案
            answer_content = answer.find('div', attrs={'class': 'zm-editable-content clearfix'})
            print('答案：', answer_content.string)

def main() :
    _xsrf, session = login('allotory@gmail.com', 'zhseverus1258740', kill_captcha)
    question_info(session, '43623869')
    print()
    answers_info(session, '43623869')

if __name__ == '__main__' :
    main()