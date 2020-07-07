
import os

# Socket Definition
socket_path = 'unix:/tmp/gunicorn.sock'
bind = socket_path
# bind = '127.0.0.1:' + str(os.getenv('PORT', 9876))
proc_name = 'Infrastructure-Practice-Flask'
workers = 1
