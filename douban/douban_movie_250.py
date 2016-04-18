# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'https://movie.douban.com/top250'

def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }
    data = requests.get(url).content
    return data

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    movie_name_list = []

    movie_ol_list = soup.find('ol', attrs={'class': 'grid_view'})
    movie_li_list = movie_ol_list.find_all('li')
    for movie_li in movie_li_list:
        movie_detail_div = movie_li.find('div', attrs={'class': 'hd'})
        movie_title_span = movie_detail_div.find('span', attrs={'class': 'title'})
        movie_name = movie_title_span.getText()
        movie_name_list.append(movie_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None

def main():
    url = DOWNLOAD_URL
    while url:
        html = download_page(url)
        movie_name_list, url = parse_html(html)
        print(movie_name_list)
        print('-------------')

if __name__ == '__main__':
    main()