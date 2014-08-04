#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from base import *
import os
DEBUG = True
TEMPLATE_DEBUG = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@beach-houserentals.com'
EMAIL_HOST_PASSWORD = '89708970'
EMAIL_USE_TLS = True

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
MANDRILL_API_KEY = b's6FW7sJNlG-I3Dldk6cYqA'

INTERNAL_IPS = ('127.0.0.1','189.124.196.94',)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

INSTALLED_APPS += ('djsupervisor',
                   'django_extensions',
                   'south',
                   'debug_toolbar',
                   )
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)



DJRILL_WEBHOOK_SECRET = b"VssYFIwxnedF49eB"

DJRILL_WEBHOOK_SIGNATURE_KEY = b'aF8zR3nNhKvr-vG7FQ0qjA'

DJRILL_WEBHOOK_URL = b'http://fetchmyguest.ngrok.com/webhooks/mandrill/?secret=VssYFIwxnedF49eB'

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False