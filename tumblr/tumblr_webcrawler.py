# -*- coding: utf-8 -*-

__author__ = 'Ellery Zhang'

'''
Tumblr web crawler advanced version.
'''

import urllib2
import re

class TumblrCrawler(object):

	def __init__(self, url):
		self.tumblr_url = url

	def getImage(self):
		tumblr_request = urllib2.Request(self.tumblr_url)
		tumblr_response = urllib2.urlopen(tumblr_request)
		tumblr_page = tumblr_response.read()
		#print tumblr_page
		imageList = []
		image_match = re.search(r'<div class="box animate">.*?<img src="(.*?)".*?</header', tumblr_page, re.X)
		if image_match:
			imageList = image_match.group(1)
		x = 0
		print len(imageList)
		print imageList
		for imageurl in imageList:
			if x < 10:
				print imageurl
				x += 1

tum = TumblrCrawler('http://cutelygirls.tumblr.com/')
tum.getImage()
