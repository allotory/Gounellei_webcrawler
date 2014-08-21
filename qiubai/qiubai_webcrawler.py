# -*- coding: utf-8 -*-

__author__ = 'Ellery Zhang'

'''
QiuShiBaiKe web crawler.
'''

import urllib2
import re


class QiubaiCrawler(object):
	def __init__(self):
		self.page = 1

	def get_page_content(self, page):
		qiubai_url = "http://www.qiushibaike.com/8hr/page/" + str(page)
		
		#set header
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		qiubai_header = {'User-Agent': user_agent}
		qiubai_request = urllib2.Request(qiubai_url, headers=qiubai_header)
		qiubai_response = urllib2.urlopen(qiubai_request)
		qiubai_page_content = qiubai_response.read()

		#set code to unicode
		qiubai_page_content_unicode = qiubai_page_content.decode('utf-8')

		qiubai_items = re.findall('<div.*?class="content".*?title="(.*?)">(.*?)</div>',
			qiubai_page_content_unicode, re.S)
		qiubai_content_list = []
		for item in qiubai_items:
			qiubai_content_list.append([item[0].replace('\n', ''), item[1].replace('\n', '')])
		return qiubai_content_list


qb = QiubaiCrawler()
content = qb.get_page_content(1)
for cont in content:
	print cont[0], cont[1]
