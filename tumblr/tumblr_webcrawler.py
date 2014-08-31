# -*- coding: utf-8 -*-

__author__ = 'Ellery Zhang'

'''
Tumblr web crawler advanced version.
'''

import urllib
import re

class TumblrCrawler(object):

	def __init__(self, url):
		self.tumblr_url = url

	def getImage(self):
		tumblr_page = urllib.urlopen(self.tumblr_url).read()
		imageList = []
		regex = r'<img src="(.*?)".*?>'
		image_reg = re.compile(regex)
		imageList = image_reg.findall(tumblr_page)
		x = 0
		print len(imageList)
		#print imageList
		for imageurl in imageList:
			if x < 10:
				print imageurl
				urllib.urlretrieve(imageurl,'%s.jpg' % x)
				x += 1

tum = TumblrCrawler('http://cutelygirls.tumblr.com/')
tum.getImage()
