from django.db import models

class User(modes.Model):
	STATUS = (
			  ('rn', 'running'),
			  ('wt', 'waiting'),
			  ('in', 'initialization'),
			  ('fs'), 'finished',
	)
	user_ID = models.CharField(max_length = 45, primary_key=True)
	status = models.CharField(max_length = 2, choices = STATUS)
	status_time = models.DateTimeField()