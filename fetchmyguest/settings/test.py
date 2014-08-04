#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from dev import *



########## TEST SETTINGS
TEST_RUNNER = "discover_runner.DiscoverRunner"
TEST_DISCOVER_TOP_LEVEL = PROJECT_DIR
TEST_DISCOVER_ROOT = PROJECT_DIR
TEST_DISCOVER_PATTERN = "test_*"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/test.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}
RAVEN_CONFIG = {
                'dsn': '',
}
SOUTH_TESTS_MIGRATE = False
INSTALLED_APPS += ('discover_runner',)