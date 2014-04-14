#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import os
import time
import cPickle
import MySQLdb
import gevent

import spider.collected as collected
import spider.loved as loved
import spider.merge as merge
import spider.recommend as recommend
import spider.filtered as filtered
import spider.download as download
import database.database as database
import logging
logging.basicConfig(filename = os.path.join(os.getcwd(), 'running.txt'),
					level = logging.WARNING,
					format = '%(asctime)s - %(levelname)s: %(message)s')  

sys.setrecursionlimit(50000)


reload(sys)
sys.setdefaultencoding('utf-8')
CELEBRITY_NUMBER = 200  #DEBUG using 10
FINAL_MOVIE_NUMBER = 35


#TODO time analysis 
#TODO logging system

def main(username):
	start_time = time.time()
	'''
	Return all the recommendaton movies according to the specific user's 
	collections of movies which user ranks 4/5 star and the movie stars 
	the user loves in Douban.
	'''

	celebrities_spawns=get_celebrities_spawns(username)

	loved_movies_spawns = get_loved_movies_spawns(username)


	spawns = celebrities_spawns + loved_movies_spawns
	gevent.joinall(spawns)

	loved_celebrities_spawns = get_loved_celebrities_spawns(username)
	gevent.joinall(loved_celebrities_spawns)
	logging.warning('Get all the loved movie stars')

	star_celebrities = merge.merge_the_celebrities()
	star_directors = merge.merge_the_directors()
	logging.warning('Merged the celebrities and the directors')



	for page in range(1,4):
		spawns = get_recommendation_movies_spawns(username, star_celebrities, 
												  '%s'%(page))
		gevent.joinall(spawns)
		logging.warning('actor page %s finished!'%(page))


	recommend.second_page_celebrities = recommend.third_page_celebrities = []

	for page in range(1, 4):
		spawns = get_recommendation_movies_spawns(username, star_directors, '%s'%(page),
												  role='director')	
		gevent.joinall(spawns)
		logging.warning("director page %s finished!"%(page))
	logging.warning('Get all the recommendation movies')

	#merge the recommendation movies
	movie_list = merge.merge_the_movies(recommend.movie_list)


	#filter those are not movies
	filter_movies_spawns = get_filter_movies_spawns(movie_list)
	gevent.joinall(filter_movies_spawns)

	# Fetch all celebrity images
	spawns = get_special_spawns(filtered.final_movies)
	gevent.joinall(spawns)

	
	#fetch all the movie poster picture
	filtered.final_movies = sorted(filtered.final_movies,
								   key=lambda x:x.final_score, reverse=True)
	final_movies = filtered.final_movies[0: FINAL_MOVIE_NUMBER]
	spawns = get_poster_spawns(final_movies)
	try:
		gevent.joinall(spawns)
	except AttributeError:
		#God knows the reason
		pass




	#Store the pickled final_movies to database
	pickle_movies = cPickle.dumps(final_movies)
	logging.warning('%s OK!!'%(username))
	database.insert_recommendation(username, pickle_movies)




	end_time = int(time.time() - start_time)
	logging.warning('Total time %s mins %s seconds'%(end_time/60, end_time%60))

def get_celebrities_spawns(username):
	'''Return the spawns of celebrities that user collects'''
	pages = collected.get_celebrities_pages(username)
	spawns = [gevent.spawn(collected.get_celebrities, username, start_number)
			  			   for start_number 
			  			   in xrange(0, pages, 15)]
	return spawns

def get_loved_movies_spawns(username):
	'''Return the spawns of movies that user rank 4/5 star'''
	total_pages = loved.get_movies_pages(username)
	logging.warning(total_pages)
	if total_pages > 1500:
		total_pages = 1500
	total_spawns = [gevent.spawn(loved.get_movies, username, start_number) 
					for start_number
					in xrange(0, total_pages, 30)]
	return total_spawns

def get_loved_celebrities_spawns(username):
	'''Return the spawns of celebrities according to the
		movies that user likes'''
	def get_star_spawns(star):
		choose_star = {'4':loved.four_star_movies_IDs,
					   '5':loved.five_star_movies_IDs}
		star_movies_IDs = choose_star[star]
		spawns = [gevent.spawn(loved.get_celebrities, username, 
							   star, star_movies_ID)
			      for star_movies_ID in star_movies_IDs]
		return spawns

	four_spawns = get_star_spawns('4')
	five_spawns = get_star_spawns('5')
	total_spawns = five_spawns + four_spawns
	return total_spawns

def get_recommendation_movies_spawns(username, star_celebrities, page, 
									 role='performer'):
	'''Return the spawns of movies that recommend
	   to the user'''
	page_number = {"1":0, '2':25, '3':50}
	start_number = page_number[page]
	if not star_celebrities:
		return []
	choose_celebrities = {
						  '1':star_celebrities[0:CELEBRITY_NUMBER], 
						  '2':recommend.second_page_celebrities,
						  '3':recommend.third_page_celebrities
						  }
	celebrities = choose_celebrities[page]
	celebrities_spawns = [gevent.spawn(recommend.get_movies, username, 
						  celebrity, start_number, role)
						  		for celebrity in celebrities]
	return celebrities_spawns

def get_filter_movies_spawns(movie_list):
	'''Return the spawns of movies which have been filtered'''
	movies_spawns= [gevent.spawn(filtered.get_final_movies, movie,) 
					for movie in movie_list]
	return movies_spawns

def get_special_spawns(movies):
	'''
	Return the spawns of url image of the celebrities
	# Parameters:
	* movies :the list of the final movies
	'''
	existing_celebrities = []
	spawns = []
	for movie in movies:
		for celebrity in movie.celebrities:
			if celebrity not in existing_celebrities:
				spawns.append(gevent.spawn(filtered.get_special, celebrity))
				existing_celebrities.append(celebrity)
	return spawns

def get_poster_spawns(final_movies):
	'''
	Return the spawns of getting the poster images
	# Parameters:	
	* final_moves : the final movies that recommend to the users
	'''
	spawns = [
			  download.get_poster(movie)
			  for movie in final_movies]
	return spawns

	

