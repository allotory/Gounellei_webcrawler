# -*- coding: utf-8 -*-

__author__ = 'Ellery Zhang'

'''
Tieba web crawler.
'''

import string, urllib2

def tieba(url, begin_page, end_page):
	for i in range(begin_page, end_page+1):
		#auto fullfill file name.
		fileName = string.zfill(i, 5) + '.html'
		print 'downloding page No.' + str(i) + ' and save as ' + fileName + '.'
		f = open(fileName, 'w+')
		m = urllib2.urlopen(url+ '?pn=' + str(i)).read()
		f.write(m)
		f.close()

tieba_url = str(raw_input('please input the tieba url(e.g.http://tieba.baidu.com/p/xxxxxxxxxx):\n'))
begin_page = int(raw_input('please input the begin page number:\n'))
end_page = int(raw_input('please input the end page number:\n'))

tieba(tieba_url, begin_page, end_page)