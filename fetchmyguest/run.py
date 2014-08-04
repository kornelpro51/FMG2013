#!/usr/bin/env python
from gevent import monkey
from socketio.server import SocketIOServer
import django.core.handlers.wsgi
import os
import sys
from django.db import connections

from os.path import abspath, dirname, join, normpath


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

sys.path.insert(0, DJANGO_ROOT)

monkey.patch_all()

# Since we are starting threading we have to enable a threaded db connection
connections['default'].allow_thread_sharing = True

try:
    from django.conf import settings
    PORT = settings.BIND_PORT
except:
    PORT = 8000

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fetchmyguest.settings.prod")

application = django.core.handlers.wsgi.WSGIHandler()

# sys.path.insert(0, os.path.join(settings.PROJECT_DIR, "apps"))

if __name__ == '__main__':
    print 'Listening on http://127.0.0.1:%s and on port 10843 (flash policy server)' % PORT
    print 'Sys Path: %s' % sys.path
    SocketIOServer(('', PORT), application, resource="socket.io").serve_forever()