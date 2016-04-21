# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json

DOWNLOAD_URL = 'http://www.lagou.com/jobs/positionAjax.json'

global pn 
pn = 1

def download_page(url) :
    global pn
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://www.lagou.com/zhaopin/Java/?labelWords=label',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }
    data = {'first': 'true', 'pn': pn, 'kd': 'python'}
    page = requests.post(url, params=data, headers=headers).content
    json_obj = json.loads(page.decode('utf-8'))
    return json_obj

def parse_json(json_obj) :
    result = json_obj['content']['result']
    has_next = json_obj['content']['hasNextPage']
    job_list = []
    for job in result :
        job_info = [job['positionName'], job['companyShortName'], job['salary'], job['city']]
        job_list.append(job_info)

    for job in result :
        print(job['positionName'] + ' - ' + job['companyShortName'] + ' - ' + job['salary'] + ' = ' + job['city']) 

    return job_list, has_next

def main() :
    has_next = True 
    global pn
    with open('jobs.txt', 'wb') as f:
        while has_next :
            json_obj = download_page(DOWNLOAD_URL)
            job_list, has_next = parse_json(json_obj)
            for job in job_list :
                f.write((''.join(job) + '\r\n').encode('utf-8'))
            print('page:', pn)
            pn += 1

if __name__ == '__main__' :
    main()