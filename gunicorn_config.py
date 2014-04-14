command = '/root/project/movie/bin/gunicorn'
pythonpath = '/root/project/movie/django_test'
bind = '127.0.0.1:8002'
workers = 3
worker_class = "gevent"
#ddd