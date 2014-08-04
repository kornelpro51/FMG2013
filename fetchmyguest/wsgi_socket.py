"""
######### IMPORTANT NOTE FROM http://uwsgi-docs.readthedocs.org/en/latest/Python.html ########

Copy your WSGI module into this new environment (under lib/python2.x if you do not want to modify your PYTHONPATH).

########

"""
import gevent.monkey
gevent.monkey.patch_all()
import gevent_psycopg2
gevent_psycopg2.monkey_patch()
import os

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
from socketio.server import SocketIOServer
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fetchmyguest.settings")
PORT = 8000





application = SocketIOServer(('', PORT), get_wsgi_application(), resource="socket.io", policy_server=True).serve_forever()
