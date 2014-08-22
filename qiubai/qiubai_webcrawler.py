# -*- coding: utf-8 -*-

__author__ = 'Ellery Zhang'

'''
QiuShiBaiKe web crawler.
'''

import urllib2
import re
import time
import thread


class QiubaiCrawler(object):
	def __init__(self):
		self.page = 1
		self.pages = []
		self.enable = False
		self.display = 'l'

	def get_page_content(self, page):
		url = "http://www.qiushibaike.com/8hr/page/" + str(page)
		
		#set header
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		header = {'User-Agent': user_agent}
		request = urllib2.Request(url, headers=header)
		response = urllib2.urlopen(request)
		page_content = response.read()

		#set code to unicode
		page_content_unicode = page_content.decode('utf-8')

		items = re.findall('<div.*?class="content".*?title="(.*?)">(.*?)</div>',
			page_content_unicode, re.S)
		content_list = []
		for item in items:
			content_list.append([item[0].replace('\n', ''), item[1].replace('\n', '')])
		return content_list

	def load_page(self):
		while self.enable:
			if len(self.pages) < 2:
				try:
					content_list = self.get_page_content(str(self.page))
					self.page += 1
					self.pages.append(content_list)
				except:
					print 'Unable linked to qiushibaike.com.'
			else:
				time.sleep(1)

	def show_page(self, now_page, page):
		if self.display == 'l':
			print 'press \'q\' to quit, and press \'enter\' to continue.'
			print 'Page %d' % page
			for items in now_page:
				print items[0], items[1]
				quit_input = raw_input()
				if quit_input == 'q':
					self.enable = False
					break
		else:
			print 'Page %d' % page
			for items in now_page:
				print items[0], items[1]
			print 'press \'q\' to quit, and press \'enter\' to continue.'
			quit_input = raw_input()
			if quit_input == 'q':
				self.enable = False
		

	def start(self):
		self.enable = True
		page = self.page

		display_input = raw_input('Line-by-line dispaly (L) or Page display (P):')
		self.display = display_input.lower()

		print 'loding...'
		thread.start_new_thread(self.load_page, ())

		while self.enable:
			if self.pages:
				now_page = self.pages[0]
				del self.pages[0]
				self.show_page(now_page, page)
				page += 1


qb = QiubaiCrawler()
qb.start()
