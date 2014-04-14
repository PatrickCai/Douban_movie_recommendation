#! /usr/bin/env python
# -- encoding:utf - 8 --
import sys
import os
import time
import query
import logging

from main import main 

import logging
logging.basicConfig(filename = os.path.join(os.getcwd(), 'worker_log.txt'),
					level = logging.WARNING,
					format = '%(asctime)s - %(levelname)s: %(message)s')  

REST_TIME = 5


def worker():
	now = time.time()
	logging.warning('Begin')
	while 1:
		user = query.choose_user()
		if user:
			logging.warning(user)
			main(user)
			query.change_status(user)
			this_time = time.time()
			if (this_time-now)>1800:
				logging.warning('Exit')
				raise SystemExit
			logging.warning('%s seconds!'%(REST_TIME))
			time.sleep(REST_TIME)
		else:
			this_time = time.time()
			if (this_time - now)>1800:
				logging.warning('Exit')
				raise SystemExit
			logging.warning('%s seconds!'%(REST_TIME))
			time.sleep(REST_TIME)



# with daemon.DaemonContext():
worker()











