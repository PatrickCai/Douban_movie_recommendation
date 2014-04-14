#! /usr/bin/env python
# -- encoding:utf - 8 --
import sys
from django.shortcuts import render
from django.db.models import Max
from django.http import HttpResponse
from recommendation.models import User

import query 
import cPickle
from database import database
from datetime import datetime
# Create your views here.

reload(sys)
sys.setdefaultencoding('utf-8')


def index(request):
	return HttpResponse('Hello')


def entrance(request):
	return HttpResponse('Entrance!')


def result(request, username):
	final_movies = database.get_recommendation(username)
	final_movies = cPickle.loads(final_movies)
	page = request.GET.get('page')
	print(page)
	if page and int(page)<35:#Hard code!Bad!
		page = int(page)
	else:
		page = 0
	movie = final_movies[page]
	for celebrity in movie.celebrities:
		celebrity.movies_list = [one_movie.name
								 for one_movie in celebrity.movie_loved]
		celebrity.movies = '<br/>'.join(celebrity.movies_list)
		if not celebrity.movies_list :
			celebrity.movies = u'这是你收藏的影人'
	for celebrity in movie.celebrities:
		if not celebrity.image_url:
			for performer in movie.celebrities:
				if performer.ID == celebrity.ID:
					celebrity.image_url = performer.image_url
	context = {'movie':movie, 'page':page}
	#Only select part of the celebrities
	if movie.celebrities[-1].role == 'director':
		directors = [director for director in movie.celebrities 
					if director.role=='director']
		performers = [performer for performer in movie.celebrities
					if performer.role=='performer'][0:5]
		movie.celebrities =  performers + directors
	else:
		movie.celebrities = movie.celebrities[0:10]
 
	return render(request, 'recommendation/result.html', context)
	# return HttpResponse(username)
	

def create(request):
	'''
	Return the estimated time if user does not exist
	If the user is not on the database,create the user and estimate the 
	rough time to calculate the final recommendation.If the user exists,and
	the status is 'finished' return the 'finished' status.If the existed user's
	status is 'wt' or 'rn' then also returns the estimated time
	'''


	user_ID = request.GET.get('username')
	try:
		user = User.objects.get(user_ID=user_ID)
		if user.status == 'wt' or user.status == 'rn':
			waiting_time = query.estimate_time()
			return HttpResponse(waiting_time)
		else:
			waiting_time = 0
			return HttpResponse(waiting_time)
	except User.DoesNotExist as e:
		status = 'wt'
		waiting_number = query.get_waiting_number()
		user = User.objects.create(
			   	user_ID=user_ID, status=status, status_time=None,
		   		waiting_number=waiting_number, register_time=datetime.now(),
		   		)
		waiting_time = query.estimate_time()
		return HttpResponse(waiting_time)

















