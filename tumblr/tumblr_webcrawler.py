# -*- coding: utf-8 -*-

__author__ = 'Ellery Zhang'

'''
Tumblr web crawler advanced version.
'''

import urllib
import re

class TumblrCrawler(object):

	def __init__(self, url, begin, end):
		self.tumblr_url = url
		self.begin_page = begin
		self.end_page = end

	def getImage(self):
		for i in range(self.begin_page, self.end_page+1):
			tumblr_page = urllib.urlopen(self.tumblr_url + 'page/' + str(i)).read()
			print self.tumblr_url + 'page/' + str(i)
			imageList = []
			#original image, this is thumb in cutelygirls.tumblr.com 
			regex = r'<img src="(.*?)".*?>'
			#original image in cutelygirls.tumblr.com
			#regex_ooriginal_inCG = r'href="(.*?)" title="Zoom">'
			image_reg = re.compile(regex)
			imageList = image_reg.findall(tumblr_page)
			x = 0
			print len(imageList)
			#print imageList
			for imageurl in imageList:
				urllib.urlretrieve(imageurl,'%s_%s.jpg' % (i, x))
				x += 1

tum = TumblrCrawler('http://cutelygirls.tumblr.com/', 1, 2)
tum.getImage()
