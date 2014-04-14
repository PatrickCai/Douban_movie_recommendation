#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys

from doulist.doulist import Celebrities_list

reload(sys)
sys.setdefaultencoding('utf-8')

class Movie(object):
	def __init__(self, ID, name=None):
		self.ID = ID
		self.name = name
	def __eq__(self, other):
		return self.ID == other.ID

	def __hash__(self):
		return hash(self.ID)


class Recommend_movie(Movie):
	def __init__(self, ID, name, star, score=0) :
		super(Recommend_movie, self).__init__(ID, name)
		self.celebrities = Celebrities_list()
		self.directors = Celebrities_list()
		self.star = star
		self.original_score = score
		self.final_score = 0
		self.comment = []
		self.poster_url = None
	def add_original_score(self, score):
		self.original_score += score

	def add_celebrity(self, celebrity):
		self.celebrities.append(celebrity)




	def __eq__(self, other):
		return self.ID == other.ID

	def __hash__(self):
		return hash(self.ID)

	def __setattr__(self, name, value):
		self.__dict__[name] = value
