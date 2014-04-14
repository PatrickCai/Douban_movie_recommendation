#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import requests 
import re
import cPickle
import random

import gevent

import gevent.monkey
gevent.monkey.patch_socket()

reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
class Daili(object):
	def __init__(self, daili):

		current_daili = re.search(u'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{2,6}', daili).group()
		company = re.search(u'[\u4e00-\u9fa5]+', daili).group()
		self.daili = current_daili
		self.company = company

	def __eq__(self, other):
		return self.company == other.company

	def __hash__(self):
		return hash(self.company)		

def get_daili():
	dailis = []
	def get_dailis(i):
		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:27.0) Gecko/20100101 Firefox/27.0',
					   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					   'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
					   'Accept-Encoding': 'gzip, deflate',
						'DNT': '1',
						'Connection': 'keep-alive'}

			r = requests.get('http://www.youdaili.cn/Daili/http/1863_%s.html'%(i), timeout=5 , headers=headers)
			print(r.url)
			soup = BeautifulSoup(r.content)
			all_html = soup.find('div', class_='cont_font').text
			result = re.findall(u'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{2,6}@HTTP#[\u4e00-\u9fa5]+', all_html)
			dailis.extend(result)

		except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
			pass
	daili_spawns = [gevent.spawn(get_dailis, i) for i in range(2,9)]
	gevent.joinall(daili_spawns)
	random.shuffle(dailis)

	good_dailis = []
	dailis = set([Daili(daili) for daili in dailis])
	dailis = [daili.daili for daili in dailis]
	def try_proxy(daili, timeout):
		proxies = {'http': 'http://%s'%(daili)}
		try:
			req = requests.get('http://movie.douban.com/celebrity/1053569/movies?start=25&format=text&sortby=vote&role=A',
								 proxies = proxies, timeout=timeout)
			if req.status_code == 200:
				good_dailis.append(daili)
				print('%s'%(proxies))
			else:
				print('fail%s'%(req.status_code))
		except 	(requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
			print('fail')
			pass
	proxy_spawns = [gevent.spawn(try_proxy, daili, 5) for daili in dailis]
	gevent.joinall(proxy_spawns)
	random.shuffle(good_dailis)
	cPickle.dump(good_dailis, open('daili', 'w'))
	print(len(good_dailis))
	good_dailis = []
	best_spawns = [gevent.spawn(try_proxy, daili, 1) for daili in dailis ]
	gevent.joinall(best_spawns)
	random.shuffle(good_dailis)
	print(len(good_dailis))
	cPickle.dump(good_dailis, open('best_daili', 'w'))


	print(good_dailis)

if __name__ == '__main__':
	# pass
	get_daili()