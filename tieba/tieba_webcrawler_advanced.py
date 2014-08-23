# -*- coding: utf-8 -*-

__author__ = 'Ellery Zhang'

'''
Tieba web crawler advanced version.
'''

import urllib2
import re
import string

class Tieba_crawler(object):

	def __init__(self, url):
		self.tieba_url = url + '?see_lz=1'
		self.datas = []

	def tieba(self):
		#read page and decode to utf-8
		tieba_request = urllib2.Request(self.tieba_url)
		tieba_response = urllib2.urlopen(tieba_request)
		tieba_page = tieba_response.read().decode('gbk')
		#total page
		total_page = self.page_counter(tieba_page)

	def page_counter(self, tieba_page):
		#会在字符串内查找模式匹配,只到找到第一个匹配然后返回，如果字符串没有匹配，则返回None。
		tieba_match = re.search(r'class="red">(\d+?)</span>', tieba_page, re.S)
		if tieba_match:
			total_page = int(tieba_match.group(1))
			print 'Crawler robot:Finding %d page content.' % total_page
		else:
			totle_page = 0
			print 'Crawler robot:Sorry,unkown max page!'
		return total_page

#tieba_id = raw_input('please input the tieba id:')
tieba_id = 2222693696
tieba_url = 'http://tieba.baidu.com/p/' + str(tieba_id)
crawler = Tieba_crawler(tieba_url)
crawler.tieba()
