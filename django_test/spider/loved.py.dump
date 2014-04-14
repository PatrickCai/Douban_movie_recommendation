#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import re
import os
dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

from bs4 import BeautifulSoup

from spider import get_soup

from role.celebrity  import Celebrity
from role.movie import Movie
from doulist.doulist import Doulist, Celebrities_list, Movie_list

import gevent.monkey
gevent.monkey.patch_socket()

reload(sys)
sys.setdefaultencoding('utf-8')

def get_movies_pages(username):
	url = 'http://movie.douban.com/people/%s/collect?&mode=list'%(username)
	soup = get_soup(url, timeout=1, priority='high')
	title_text = soup.title.text
	movies_pages = (int(re.search('\((\d+)\)', title_text).group(1))/30 + 1)*30
	return movies_pages

four_star_movies_IDs = Doulist()
five_star_movies_IDs = Doulist()
movies_have_seen = Movie_list()

def get_movies(username, start_number):
	url = 'http://movie.douban.com/people/%s/collect?start=%s&mode=list'%(username, start_number)
	soup = get_soup(url, timeout=10)
	htmls = soup.findAll('li', id=re.compile('list\d{7,8}'),  class_=re.compile('item')) 
	for html in htmls:
		star_html = html.find('span', class_=re.compile('rating\d-t'))
		if star_html:
			star_html = star_html['class'][0]
		else:
			star_html = None
		movie_ID = re.search('\d{7,8}', html['id']).group()
		if star_html == 'rating5-t':
			five_star_movies_IDs.append(movie_ID)
		elif star_html == 'rating4-t':
			four_star_movies_IDs.append(movie_ID)
		movies_have_seen.append(Movie(movie_ID))
	print('2.start number %s'%(start_number))


star_celebrities = Celebrities_list()
star_directors = Celebrities_list()
def get_celebrities(username, star, star_movie_ID):
	url = 'http://movie.douban.com/subject/%s/'%(star_movie_ID)
	soup = get_soup(url, timeout=15)
	#celebrity
	celebrity_htmls = soup.findAll('a', {'rel':'v:starring'}, href=re.compile('/celebrity/\d{7}'), limit=4)
	page_celebrity_IDs = [re.search('(\d{7})', celebrity_html['href']).group() for celebrity_html in celebrity_htmls]
	page_celebrity_names =[celebrity.text for celebrity in celebrity_htmls]
	#TODO!the directors are not included!
	directors_htmls = soup.findAll('a', {'rel':'v:directedBy'}, href=re.compile('/celebrity/\d{7}'))
	directors_IDs = [re.search('(\d{7})', directors_html['href']).group() for directors_html in directors_htmls]
	directors_names = [director.text for director in directors_htmls]
	page_directors = [Celebrity(directors_ID, original_score=star, name=name, role='director')
						 for directors_ID, name in zip(directors_IDs, directors_names) ]
	
	page_celebrities = [Celebrity(page_celebrity_ID, original_score=star, name=name)
						 for page_celebrity_ID,name in zip(page_celebrity_IDs, page_celebrity_names)]
	#movie information
	movie_name =soup.find('span', {'property':'v:itemreviewed'}).text 
	movie = Movie(star_movie_ID, movie_name)
	for page_celebrity in page_celebrities:
		page_celebrity.add_loved_movie(movie) 
	for page_director in page_directors:
		page_director.add_loved_movie(movie)

	star_directors.extends(page_directors, movie, star)
	star_celebrities.extends(page_celebrities, movie, star)
	print('3.OK %s movie ID'%(star_movie_ID))


if __name__ == '__main__':
	get_celebrities('cliffedge', '0', '1418834')