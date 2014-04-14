#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import re
import os
father = os.path.pardir
dirname = os.path.split(os.path.realpath(__file__))[0]
dirname = os.path.join(dirname, father)
sys.path.append(dirname)
from role.celebrity import Celebrity

class Doulist(list):
	def __init__(self):
		super(Doulist, self).__init__()

class Celebrities_list(list):
	def __init__(self, cele_list=None):
		if cele_list:
			super(Celebrities_list, self).__init__(cele_list)
		else:
			super(Celebrities_list, self).__init__()


	def extends(self, celebrities, movie, star):
		for celebrity in self:
			if celebrity in celebrities:
				celebrity.add_loved_movie(movie)
				celebrity.add_original_score(star)
				celebrities.remove(celebrity)
		super(Celebrities_list, self).extend(celebrities)


	def add(self, celebrities):
		'''self is the star_celebrities , celebrities is the collected '''
		union = set(self) & set(celebrities)
		for celebrity in self:
			if celebrity in union:
				celebrity.add_original_score('5')
		union_left = Celebrities_list(set(celebrities) - union)
		return self + union_left

class Movie_list(list):
	def __init__(self, movie_list=None):
		if movie_list:
			super(Movie_list, self).__init__(movie_list)
		else:
			super(Movie_list, self).__init__()
			
	def extends(self, movie_list, celebrity):
		for movie in self:
			if movie in movie_list:
				movie.add_celebrity(celebrity)
				movie.add_original_score(celebrity.final_score)
				movie_list.remove(movie)
		super(Movie_list, self).extend(movie_list)

	

if __name__ == '__main__':
	dd = Celebrity('22')
	df = Celebrity('22')
	de = Celebrity('23')
	dr = Celebrity('24')

	kk = Celebrities_list()
	kk.append(dd)
	kk.append(de)

	kf = Celebrities_list()
	kf.append(df)
	kf.append(dr)

	kk.extends(kf, 'dd', '2')
	print(kk)

