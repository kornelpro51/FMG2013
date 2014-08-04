#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from base import *
import os

DEBUG = False

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

MANDRILL_API_KEY = 'jZ_fMmOehPSoRTxuC3GyfA'

RAVEN_CONFIG = {
                'dsn': 'https://190e4db4576d4897ad6bb1bdc365a9eb:2895cea11e4743a3b84a1f753d3dc953@app.getsentry.com/16951',
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.getenv('MEMCACHE_LOCATION', '127.0.0.1:11211'),
    }
}

INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

DJRILL_WEBHOOK_SECRET = b"VssYFIwxnedF49eB"

DJRILL_WEBHOOK_SIGNATURE_KEY = b'_fWlJ29iJJDJwK0pRqCB2w'

DJRILL_WEBHOOK_URL = b'http://agent.fetchmyguest.com/webhooks/mandrill/?secret=VssYFIwxnedF49eB'

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False