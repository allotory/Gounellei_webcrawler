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
		self.myTool = HTML_Tool() 

	def tieba(self):
		#read page and decode to utf-8
		tieba_request = urllib2.Request(self.tieba_url)
		tieba_response = urllib2.urlopen(tieba_request)
		tieba_page = tieba_response.read().decode('gbk')
		#total page
		total_page = self.find_total_page(tieba_page)
		#title
		tieba_title = self.find_title(tieba_page)
		print tieba_title
		#save
		self.save_data(self.tieba_url, tieba_title, total_page)

	def find_total_page(self, tieba_page):
		#会在字符串内查找模式匹配,只到找到第一个匹配然后返回，如果字符串没有匹配，则返回None。
		tieba_match = re.search(r'class="red">(\d+?)</span>', tieba_page, re.S)
		if tieba_match:
			total_page = int(tieba_match.group(1))
			print 'Crawler robot:Finding %d page content.' % total_page
		else:
			totle_page = 0
			print 'Crawler robot:Sorry,unkown max page!'
		return total_page

	def find_title(self, tieba_page):
		tieba_match = re.search(r'<h1.*?>(.*?)</h1>', tieba_page, re.S)
		tieba_title = 'no title.'
		if tieba_match:
			tieba_title = tieba_match.group(1)
		else:
			print 'Crawler robot:Sorry, unkown title!'
		# 文件名不能包含以下字符： \ / ： * ? " < > |
		tieba_title = tieba_title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')
		return tieba_title

	def save_data(self, tieba_url, tieba_title, total_page):
		tieba_url = tieba_url + '&pn='
		#deal tieba page and save to list
		for i in range(1, total_page+1):
			print 'Crawler robot:Loding page %d' % i
			tieba_page = urllib2.urlopen(tieba_url + str(i)).read()
			#get content from source page
			tieba_items = re.findall('id="post_content.*?>(.*?)</div>', tieba_page.decode('gbk'), re.S)
			for item in tieba_items:
				data = self.myTool.Replace_Char(item.replace('\n', '').encode('gbk'))
				self.datas.append(data + '\n')
		#save to local
		f = open(tieba_title + '.txt', 'w+')
		f.writelines(self.datas)
		f.close()
		print 'Download complete.'

class HTML_Tool:
	# 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
	BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")

	# 用非 贪婪模式 匹配 任意<>标签
	EndCharToNoneRex = re.compile("<.*?>")

	# 用非 贪婪模式 匹配 任意<p>标签
	BgnPartRex = re.compile("<p.*?>")
	CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
	CharToNextTabRex = re.compile("<td>")

	# 将一些html的符号实体转变为原始符号
	replaceTab = [("&lt;","<"),("&gt;",">"),("&amp;","&"),("&amp;","\""),("&nbsp;"," ")]

	def Replace_Char(self,x):
		x = self.BgnCharToNoneRex.sub("",x)
		x = self.BgnPartRex.sub("\n    ",x)
		x = self.CharToNewLineRex.sub("\n",x)
		x = self.CharToNextTabRex.sub("\t",x)
		x = self.EndCharToNoneRex.sub("",x)

		for t in self.replaceTab:  
			x = x.replace(t[0],t[1])  
		return x


#tieba_id = raw_input('please input the tieba id:')
tieba_id = 2222693696
tieba_url = 'http://tieba.baidu.com/p/' + str(tieba_id)
print tieba_url
crawler = Tieba_crawler(tieba_url)
crawler.tieba()
