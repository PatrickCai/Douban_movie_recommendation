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
from role.comment import Comment

reload(sys)
sys.setdefaultencoding('utf-8')

final_movies = Movie_list()
def get_final_movies(movie):
	def find_author_comment(star):
		star = soup.find('span', class_=("allstar%s0 rating"%(star)))
		if star:
			comment = star.parent.parent.next_sibling.next_sibling.next
			comment = str(comment)
			author = star.previous_sibling.previous_sibling.text
		else:
			comment = None
			author = None
		return comment, author
	def get_comment():
		is_movie = not bool(soup.find('div', class_='episode_list'))
		
		audience_number = soup.find('span', {'property':'v:votes'})
		if audience_number:
			audience_number = audience_number.text
		else:
			audience_number = 0
		has_enough_audience = True if int(audience_number)>250 else False
		if is_movie and has_enough_audience:
			four_comment,four_author = find_author_comment(4) 
			five_comment,five_author = find_author_comment(5) 
			if not five_comment:
				movie.comment = Comment(four_comment, four_author, 4)
			else:
				movie.comment = Comment(five_comment, five_author, 5)
			return movie.comment

	url = 'http://movie.douban.com/subject/%s/'%(movie.ID)
	soup = get_soup(url, timeout=8)
	comment = get_comment()
	#Poster url
	poster_url = soup.find('img', {'rel':'v:image'}, 
							{'title':u'点击看更多海报'})['src']
	if comment:
		movie.poster_url = poster_url
		print('5.Ok %s'%(movie.ID))
		final_movies.append(movie)

existing_movies = []
def get_special(celebrity):
	url = 'http://movie.douban.com/celebrity/%s/'%(celebrity.ID)
	soup = get_soup(url, timeout=5)
	image_url = soup.find('img', title=u'点击看大图')['src']
	pp = re.compile('medium')
	image_url = pp.sub('small', image_url)
	celebrity.image_url = image_url
	print('6.celebrity%s image'%(celebrity.ID))
	

if __name__ == '__main__':
	get_final_movies(Recommend_movie(1871852, 'ddd', 4))
