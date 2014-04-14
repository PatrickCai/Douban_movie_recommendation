from django.conf.urls import patterns, url

from recommendation import views

urlpatterns = patterns('',
				url(r'', views.index, name='index')
				
		)