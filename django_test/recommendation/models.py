#! /usr/bin/env python
# -- encoding:utf - 8 --

from django.db import models
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your models here.
class User(models.Model):
	STATUS = (
			  ('rn', 'running'),
			  ('wt', 'waiting'),
			  ('in', 'initialization'),
			  ('fs', 'finished'),
	)
	user_ID = models.CharField(max_length = 45, primary_key=True)
	status=models.CharField(max_length=2, choices=STATUS)
	status_time = models.DateTimeField()
	waiting_number = models.IntegerField()
	register_time = models.DateTimeField()
		
	class Meta:
		db_table = 'user'
