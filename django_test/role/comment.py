#! /usr/bin/env python
# -- encoding:utf - 8 --

import sys
import os
import MySQLdb
import cPickle
dirname = os.path.dirname(sys.path[0])
sys.path.append(dirname)

reload(sys)
sys.setdefaultencoding('utf-8')

class Comment(object):
	def __init__(self, content, author, star):
		self.name = content
		self.author = author
		self.star = star

if __name__ == '__main__':
	host = 'localhost'
	user = 'root'
	passwd = ''
	db = 'test'
	port = 3306

	conn = MySQLdb.connect(host=host, user=user, passwd=passwd,db=db, port=port)
	cur = conn.cursor()
	value = (1,)
	cur.execute('select ddd from test where s=%s' , value)
	ddd = cur.fetchone()[0]
	ddd = cPickle.loads(ddd)
	for dd in ddd:
		print(dd.ID)

