# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'https://book.douban.com/top250'

def download_page(url) :
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }
    page = requests.get(url, headers=headers).content
    return page

def parse_html(html) :
    soup = BeautifulSoup(html, 'html.parser')

    book_name_list = []

    book_list_div = soup.find('div', attrs={'class': 'indent'})
    book_table_list = book_list_div.find_all('table')
    for book_table in book_table_list : 
        book_detail = book_table.find('div', attrs={'class': 'pl2'})
        book_name = book_detail.find('a').getText(strip=True)
        print(book_name)
        book_name_list.append(book_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page :
        return book_name_list, next_page['href']

    return book_name_list, None


def main() :
    url = DOWNLOAD_URL
    with open('book.txt', 'a') as f :
        while url :
            page = download_page(url)
            book_name_list, url = parse_html(page)
            for book_name in book_name_list :
                f.write(book_name + '\r\n')
                print(book_name)

if __name__ == '__main__' :
    main()