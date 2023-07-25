# gunicorn_config.py

import multiprocessing

# Set the application directory
chdir = '.'

# Gunicorn configuration
bind = '0.0.0.0:5000'
workers = multiprocessing.cpu_count() * 2 + 1
