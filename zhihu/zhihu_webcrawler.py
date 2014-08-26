# -*- coding: utf-8 -*-

__author__ = 'Ellery Zhang'

'''
Zhihu web crawler advanced version.
'''

import urllib2
import re

class ZhihuCrawler(object):

	def get_answer(self, page_id):
		url = "http://www.zhihu.com/question/" + str(page_id)
		
		#set header
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		header = {'User-Agent': user_agent}
		request = urllib2.Request(url, headers=header)
		response = urllib2.urlopen(request)
		page_content = response.read()

		#set code to unicode
		page_content_unicode = page_content.decode('utf-8')

		items = re.findall('<a data-tip=".*?" href="/people/.*?">(.*?)</a>.*?class="zu-question-my-bio">(.*?)</strong>.*?<div class=".*?zm-editable-content clearfix">(.*?)</div>.*?<a class="answer-date-link.*?>(.*?)</a>',
			page_content_unicode, re.S)
		return items

zu = ZhihuCrawler()
content = zu.get_answer(24997123)
for c in content:
	print c[0] + '----' + c[1] + ':'
	print c[2].lstrip().rstrip() + '----' + c[3]
	print 
