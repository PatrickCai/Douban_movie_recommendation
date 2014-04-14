#! /usr/bin/env python
# -- encoding:utf - 8 --
import sys
from recommendation.models import User
from django.db.models import Max
from main import main
import time
from datetime import datetime
from django.db.models import F
reload(sys)
sys.setdefaultencoding('utf-8')

ONE_RUNNING_TIME = 480
REST_TIME = 30

def _get_max_waiting_number():
	'''
	Return the max waiting number
	'''
	user = User.objects.filter(waiting_number__gte=-1)
	if user:
		user = user.aggregate(Max('waiting_number'))
		user_number = user.values()[0]
	else:
		return -1
	return user_number

def estimate_time():
	'''
	Return the waiting time in seconds
	'''
	user_number = _get_max_waiting_number()
	waiting_time = ONE_RUNNING_TIME * (user_number+1)
	return waiting_time

def get_waiting_number():
	'''
	Return the waiting number 
	'''
	user_number = _get_max_waiting_number()
	user_number += 1
	return user_number

def choose_user():
	'''
	Return the user_ID which will be running this time,and change its 
	status to running
	'''
	user = User.objects.filter(waiting_number=0)
	if user:
		if user[0].status=='rn':
			return 
		user.update(status='rn')
		user = user[0]
		return user.user_ID
	else:
		return None

def change_status(user_ID):
	'''
	Change one user's status from rn to fs,status_time,and all users'
	waiting number
	'''
	user = User.objects.filter(user_ID=user_ID)
	user.update(
		status='fs', status_time=datetime.now(), waiting_number=-1
		)
	users = User.objects.filter(waiting_number__gt=0)
	users.update(waiting_number=F('waiting_number')-1)







