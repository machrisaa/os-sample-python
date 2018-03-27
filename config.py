import os

# workers = int(os.environ.get('GUNICORN_PROCESSES', '3'))
# threads = int(os.environ.get('GUNICORN_THREADS', '1'))
workers = 1
threads = 1

preload = True

forwarded_allow_ips = '*'
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}
