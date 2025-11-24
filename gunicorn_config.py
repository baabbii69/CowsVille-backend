"""
Gunicorn configuration file for Cowsville Django application
"""

import multiprocessing
import os

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Increased timeout
keepalive = 2

# Logging - use absolute paths
accesslog = os.path.join(BASE_DIR, "logs", "gunicorn_access.log")
errorlog = os.path.join(BASE_DIR, "logs", "gunicorn_error.log")
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "cowsville"

# Server mechanics
daemon = False
pidfile = os.path.join(BASE_DIR, "logs", "gunicorn.pid")
umask = 0
user = None
group = None
tmp_upload_dir = None

# Preload app for faster worker spawn
preload_app = True

# SSL (if needed)
# keyfile = None
# certfile = None
