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

def user_info(session, url_token) :
    resp = session.get('https://www.zhihu.com/people/' + url_token + '/about')
    soup = BeautifulSoup(resp.content, 'html.parser')

    name = soup.find('a', attrs={'class': 'name'})
    bio = soup.find('span', attrs={'class': 'bio'})
    location = soup.find('span', attrs={'class': 'location item'})
    business = soup.find('span', attrs={'class': 'business item'})
    employment = soup.find('span', attrs={'class': 'employment item'})
    position = soup.find('span', attrs={'class': 'position item'})
    education = soup.find('span', attrs={'class': 'education item'})
    education_extra = soup.find('span', attrs={'class': 'education-extra item'})
    description = soup.find_all('span', attrs={'class': 'content'})[0]

    print('------- 用户信息 -------')
    print('用户：', name.string)
    print('简介：', bio.string)
    print('居住信息：', location.attrs['title'])
    print('行业信息：', business.attrs['title'])
    print('公司信息：', employment.attrs['title'])
    print('职位信息：', position.attrs['title'])
    print('毕业院校：', education.attrs['title'])
    print('专业方向：', education_extra.attrs['title'])
    print('个人描述：', description.string.strip())
    print()

    profile = soup.find('div', attrs={'class': 'profile-navbar clearfix'})
    asks = profile.find('a', attrs={'href': '/people/'+url_token+'/asks'})
    answers = profile.find('a', attrs={'href': '/people/'+url_token+'/answers'})
    posts = profile.find('a', attrs={'href': '/people/'+url_token+'/posts'})
    collections = profile.find('a', attrs={'href': '/people/'+url_token+'/collections'})
    logs = profile.find('a', attrs={'href': '/people/'+url_token+'/logs'})

    reputation_wrap = soup.find('div', attrs={'class': 'zm-profile-module zm-profile-details-reputation'})
    reputation = reputation_wrap.find_all('strong')

    print('提问：', asks.find('span').string)
    print('回答：', answers.find('span').string)
    print('文章：', posts.find('span').string)
    print('收藏：', collections.find('span').string)
    print('公共编辑：', logs.find('span').string)
    print()

    print('赞同：', reputation[0].string)
    print('感谢：', reputation[1].string)
    print('被收藏：', reputation[2].string)
    print('分享：', reputation[3].string)

def main() :
    _xsrf, session = login('allotory@gmail.com', 'zhseverus1258740', kill_captcha)
    user_info(session, 'rednaxelafx')

if __name__ == '__main__' :
    main()