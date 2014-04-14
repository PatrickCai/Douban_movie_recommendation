#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import re
import os
father = os.path.pardir
dirname = os.path.split(os.path.realpath(__file__))[0]
dirname = os.path.join(dirname, father)
sys.path.append(dirname)

import requests
from bs4 import BeautifulSoup

from role.celebrity  import Celebrity
from spider import get_soup

from doulist.doulist import Celebrities_list
reload(sys)
sys.setdefaultencoding('utf-8')

celebrities = Celebrities_list()
def get_celebrities(username, start_number):
	url = 'http://movie.douban.com/people/%s/celebrities?start=%s'%(username, start_number)
	soup = get_soup(url, timeout=10)
	page_celebrities = soup.findAll('a', href=re.compile('http://movie.douban.com/celebrity/\d{7}/$'))
	page_celebrities = [re.search('\d{7}', celebrity['href']).group() 
						for celebrity in page_celebrities 
						if page_celebrities.index(celebrity)%2 == 0]

	names_html = soup.findAll('em')
	names = [unicode(name.text) for name in names_html]
	page_celebrities = [Celebrity(page_celebrity, collect_or_watch='collect', 
						original_score=5, name=name) for page_celebrity,name in 
						zip(page_celebrities, names)]
	celebrities.extend(page_celebrities)
	print('1.collect page%s OK'%(start_number))

def get_celebrities_pages(username):
	url = 'http://movie.douban.com/people/%s/celebrities'%(username)
	print('Start!')
	soup = get_soup(url, priority='high', timeout=10)
	title = soup.title.text
	pages = int(re.search('\((\d+)\)$', title).group(1))	
	return pages

if __name__ == '__main__':
	get_celebrities('cliffedge', '0')



