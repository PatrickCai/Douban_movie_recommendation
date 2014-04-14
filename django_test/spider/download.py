#! /usr/bin/env python
# -- encoding:utf - 8 --


import sys
import os
from django.conf import settings
father = os.path.pardir
dirname = os.path.split(os.path.realpath(__file__))[0]
dirname = os.path.join(dirname, father)
sys.path.append(dirname)

import requests
from database import database
from role import movie 
import spider
reload(sys)
sys.setdefaultencoding('utf-8')

# r = requests.get('http://img3.douban.com/view/movie_poster_cover/spst/public/p2174990264.jpg', stream=True)
# if r.status_code == 200:
# 	with open('1.jpg', 'wb') as tt:
# 		for chunk in r.iter_content():
# 			tt.write(chunk)


def _get_image(url, movie_ID):
	'''
	Return the image's file path ,store the image's file
	# Parameters:
	* url : poster's url
	* movie_ID : movie_ID used for naming the image file
	'''

	content = spider.get_soup(url, timeout=5, priority='high',
							 content=True)
	#Warning!It is really a bad design!!
	image_url = os.path.join(dirname, 'media/poster/%s.jpg'%(movie_ID))
	with open(image_url, 'wb') as tt:
		tt.write(content)
	image_url = '/picture/poster/%s.jpg'%(movie_ID)
	return image_url

def get_poster(movie):
	'''
	Inquire whether the poster is already in the database get the poster
	image and store it in the database if it is not in.
	# Parameters:
	* movie : To get this movie's poster image
	'''
	url = movie.poster_url
	movie_ID = movie.ID
	do_exist, poster_path = database.do_exist(movie_ID)
	if  do_exist:
		movie.poster_url = poster_path
	else:
		poster_path = _get_image(url, movie_ID)
		database.insert_image(movie_ID, poster_path)
		movie.poster_url = poster_path
	print('6 OK %s poster'%(movie_ID))



if __name__ == '__main__':
	_get_image('http://img5.douban.com/view/movie_poster_cover/spst/public/p2175207456.jpg', 3333)






