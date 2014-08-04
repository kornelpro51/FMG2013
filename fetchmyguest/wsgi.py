"""
WSGI config for learnsocketio project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

######### IMPORTANT NOTE FROM http://uwsgi-docs.readthedocs.org/en/latest/Python.html ########

Copy your WSGI module into this new environment (under lib/python2.x if you do not want to modify your PYTHONPATH).

########
"""
import os
site_dir = os.getenv('SITE_DIR', '')
if site_dir:
    import site
    site.addsitedir('/srv/Envs/fetchmyguest/lib/python2.7/site-packages')
# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fetchmyguest.settings.prod")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
