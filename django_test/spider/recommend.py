#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import os
import re

import gevent.monkey
gevent.monkey.patch_socket()

father = os.path.pardir
dirname = os.path.split(os.path.realpath(__file__))[0]
dirname = os.path.join(dirname, father)
sys.path.append(dirname)
from doulist.doulist import Movie_list
from spider import get_soup

from role.movie import Recommend_movie

reload(sys)
sys.setdefaultencoding('utf-8')

movie_list = Movie_list()
second_page_celebrities = []
third_page_celebrities = []
def get_movies(username, celebrity, start_number, role='performer'):
	choose_role = {'performer':'A', 'director':'D'}
	movie_role = choose_role[role]
	url = 'http://movie.douban.com/celebrity/%s/movies?start=%s&format=text&sortby=vote&role=%s'%(celebrity.ID, start_number, movie_role)
	soup = get_soup(url, timeout=8)
	movie_htmls = soup.findAll('a', href=re.compile('http://movie.douban.com/subject/\d{7,8}'))
	star_htmls = soup.findAll('span', class_='rating_nums')

	movie_IDs = [re.search('\d{7,8}', movie_html['href']).group() for movie_html in movie_htmls]
	movie_names = [movie_html.text for movie_html in movie_htmls]
	stars = [star_html.text for star_html in star_htmls]
	recommend_movies = Movie_list([Recommend_movie(movie_ID, movie_name, star, score=celebrity.final_score) 
						for movie_ID, movie_name, star in zip(movie_IDs,
																 movie_names, stars)])

	choose_list = {0:second_page_celebrities, 25:third_page_celebrities, 50:[]}
	exist_html = soup.find("span", class_='allstar00')
	if not exist_html:
		choose_list[start_number].append(celebrity)

	for movie in recommend_movies:
		movie.add_celebrity(celebrity)


	movie_list.extends(recommend_movies, celebrity)
	print('4.celebrity ID %s OK '%(celebrity.ID))


if __name__ == '__main__':
	pass