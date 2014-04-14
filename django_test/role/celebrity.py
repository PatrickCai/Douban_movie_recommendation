#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import collections

reload(sys)
sys.setdefaultencoding('utf-8')

class Celebrity(object):
	def __init__(self, ID, collect_or_watch='watch', 
				original_score=0,name=None, role='performer',
				image_url=None):
		self.ID = ID
		self.name = name
		self.role = role
		self.collect_or_watch = collect_or_watch
		self.original_score = int(original_score) - 2
		self.final_score = None
		self.movie_loved = []
		self.image_url = image_url

	def add_loved_movie(self, movie):
		self.movie_loved.append(movie)
		
	def add_original_score(self, star):
		self.original_score += (int(star)-2)

	def __eq__(self, other):
		return self.ID == other.ID

	def __hash__(self):
		return hash(self.ID)

	def __setattr__(self, name, value):
		self.__dict__[name] = value

if __name__ == '__main__':
	a = Celebrity('12')
	b = Celebrity('13')
	dd = [a, 'dd', b]
	df = [a, 'df']
	print(list(set(dd).difference(set(df))))
	# if b in dd:
	# 	print('yes')
