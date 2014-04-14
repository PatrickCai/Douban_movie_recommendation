#! /usr/bin/env python
# -- encoding:utf - 8 --

import MySQLdb
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')




host = 'localhost'
user = 'root'
# passwd = ''
db = 'recommendation'
port = 3306



def _connect():
	'''
	Connect to the database
	'''
	conn = MySQLdb.connect(host=host, user=user, passwd=passwd,db=db, port=port)
	cur = conn.cursor()
	return (conn, cur)	

def _disconnect(conn, cur):
	'''
	Close the database 
	'''
	cur.close()
	conn.close()


def do_exist(movie_ID):
	'''
	Return whether the poster is in the database
	# Parameters:
	* movie_ID : movie_ID
	'''
	(conn, cur) = _connect()
	values = [movie_ID]
	cur.execute('SELECT poster_url FROM movie_poster WHERE movie_ID=%s', values)
	result = cur.fetchone()
	do_exist = bool(result)
	if do_exist:
		poster_path = result[0]
	else:
		poster_path = None
	_disconnect(conn, cur)
	return do_exist,poster_path

def insert_image(movie_ID, poster_url):
	(conn, cur) = _connect()
	values = [movie_ID, poster_url]
	cur.execute('INSERT INTO movie_poster values (%s, %s)', values)
	conn.commit()
	_disconnect(conn, cur)

def insert_recommendation(username, pickle_movies):
	'''
	Insert the pickle_movies into the table 'recommendation'
	# Parameters:
	* pickle_movies : movies that have already pickled 
	'''
	(conn, cur) = _connect()
	values = [username,]
	cur.execute('SELECT * FROM recommendation WHERE user_ID=%s', values)
	result = cur.fetchone()
	if not result:
		values = [username, pickle_movies]
		cur.execute('INSERT INTO recommendation values (%s, %s)', values)
		conn.commit()
	else:
		values = [pickle_movies, username]
		cur.execute(
			'UPDATE recommendation SET recommendation=%s where user_ID=%s', values
			)
		conn.commit()
	_disconnect(conn, cur)

def get_recommendation(username):
	'''
	Return the pickle_movies if the user exists if not Return nothing
	'''
	(conn, cur) = _connect()
	values = [username,]
	cur.execute('SELECT * FROM recommendation WHERE user_ID = %s', values)
	result = cur.fetchone()
	if result:
		final_movies = result[1]
		return final_movies
	else:
		return None
	_disconnect(conn, cur)





if __name__ == '__main__':
	# get_recommendation('cliffedge')
	print(time.time())











