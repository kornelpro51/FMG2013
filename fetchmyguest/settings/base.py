#-*- coding: utf-8 -*-

from __future__ import unicode_literals  # This line is to avoid unicode string problems and Python 3 compatibility
import dj_database_url
import djcelery
import os
from os.path import dirname
gettext = lambda s: s
PROJECT_DIR = os.path.abspath(dirname(dirname(dirname(__file__))))

#for yousuf's localhost
HOSTNAME = os.uname()[1]

BIND = "0.0.0.0:8000"
BIND_PORT = 8000

DEBUG = False
USE_ETAGS = False

MEDIA_URL = "/media/"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, "static")
MEDIA_ROOT = os.path.join(PROJECT_DIR, "media")
ADMIN_MEDIA_PREFIX = '/static/admin/'
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('paolo', 'paolo.cesare.calvi@gmail.com'),
    ('Warning', 'warning@fetchmyguest.com'),
)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='postgres://postgres:a@localhost:5432/testdb')}

DATABASES['default'].update({
    'OPTIONS': {'autocommit': True, }
})

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1.
USE_I18N = True
USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'custom_static'),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # 'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = '3i%f_7iu%3yg7lv#7#axu6-ebxs@mcsve@!(r%mc9n4%l7g-i-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    #'mezzanine.core.middleware.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cuser.middleware.CuserMiddleware',
    #'fetchmyguest.middleware.AutoLogout',
    # 'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mezzanine.pages.middleware.PageMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    #'mezzanine.core.middleware.FetchFromCacheMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AGENCY_MONTH_TARGET = int(os.getenv('AGENCY_MONTH_TARGET', '25'))

LEADS_CUT_OFF_DAYS = int(os.getenv('LEADS_CUT_OFF_DAYS', '30'))

ROOT_URLCONF = 'fetchmyguest.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'fetchmyguest.wsgi.application'

TEMPLATE_DIRS = (

    os.path.join(PROJECT_DIR, "templates"),
)

INSTALLED_APPS = (
    'mezzanine.boot',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.redirects',
    #'django.contrib.sites',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # 'grappelli.dashboard',
    # 'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # third party
    # 'debug_toolbar',


    'django_mailbox',
    'djcelery',
    #'tastypie',
    'tinymce',
    'cities_light',
    'rest_framework',
    'rest_framework_swagger',
    'djcelery_email',
    'guardian',
    'custom_user',
    'registration',
    'bootstrap_toolkit',
    'cuser',

    'django_hstore',
    'django_nvd3',
    'djangobower',
    'djrill',
    'compressor',

    # local
    'leads',
    'agencies',

    #'Mezzanine'

    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    'mezzanine.blog',
    'mezzanine.forms',
    'mezzanine.pages',
    'mezzanine.galleries',
    'mezzanine.twitter',
    #'mezzanine.accounts',
    #'mezzanine.mobile',
    #'cacheops',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    #'Mezzanine'
    'mezzanine.conf.context_processors.settings',
)

PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

ACCOUNT_ACTIVATION_DAYS = 7

DEFAULT_AGENCY_ID = 1

SEND_BROKEN_LINK_EMAILS = True

RAVEN_CONFIG = {
                'dsn': 'https://891e9dbdad71453c8b15c6f16e1489ef:8a0d1707aca64810bc1a37c80921e241@app.getsentry.com/15428',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_DIR, 'log/debug.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'log_error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_DIR, 'log/error.log'),
            'maxBytes': '16777216', # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'formatter': 'verbose'

        }
    },

    'loggers': {
        '': {
            'handlers': ['console', 'log_file', 'log_error_file', 'sentry'],
            #            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['log_error_file'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['log_error_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.django.db.backends': {
            'handlers': ['console','log_error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

# Django REST Settings
REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'DEFAULT_RENDERER_CLASSES': (
        'drf_ujson.renderers.UJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
                                'rest_framework.filters.OrderingFilter',
                                'rest_framework.filters.SearchFilter',
    ),
    'PAGINATE_BY': 25,
    'PAGINATE_BY_PARAM': 'page_size',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

ANONYMOUS_USER_ID = -1
AUTH_USER_MODEL = 'custom_user.EmailUser'

# Django Activity Stream settings
ACTSTREAM_SETTINGS = {
    'MODELS': (AUTH_USER_MODEL, 'leads.lead'),
    'MANAGER': 'actstream.managers.ActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

# Testing Settings
TESTING_PHASE = True
TESTING_EMAIL_ADDRESS = 'trolltrololol88@gmail.com'
DEFAULT_FROM_EMAIL_ADDRESS = 'info@beach-houserentals.com'
LIVE_TESTING_PHASE = False


# Email settings


DEFAULT_FROM_EMAIL = 'info@beach-houserentals.com'
EMAIL_SUBJECT_PREFIX = '[GuestRetriever]'

NEVERCACHE_KEY = False


CELERY_EMAIL_TASK_CONFIG = {
    'name': 'djcelery_email_send',
    'ignore_result': True,
    'queue': 'email',
    'rate_limit': '50/m',
}

API_LIMIT_PER_PAGE = 0


# TINYMCE Settings
TINYMCE_JS_URL = os.path.join(STATIC_ROOT, "grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, "grappelli/tinymce/jscripts/tiny_mce")
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}
TINYMCE_SETUP_JS = 'tinymce_setup/tinymce_setup.js'
#TINYMCE_SETUP_JS = os.path.join(STATIC_ROOT, "tinymce_setup/tinymce_setup.j")



DJANGO_MAILBOX_ALLOWED_MIMETYPES = [
    'text/plain',
    'text/html'
]

GRAPPELLI_ADMIN_TITLE = 'Fetchmyguest'
GRAPPELLI_ADMIN_HEADLINE = 'Fetch my leads!'

DJANGO_MAILBOX_STRIP_UNALLOWED_MIMETYPES = True

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 30
CACHE_MIDDLEWARE_KEY_PREFIX = 'fetch'

QUERY_CACHING_ENABLED = False
LEAD_GENERATION_CACHING_TIMEOUT = 3600

SOUTH_MIGRATION_MODULES = {
    'django_mailbox': 'fetchmyguest.migrations.django_mailbox',
}

OPTIONAL_APPS = (
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

SESSION_REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
SESSION_REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
SESSION_REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
REDIS_SOCKET_TIMEOUT = 0

BROKER_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
BROKER_BACKEND = "redis"
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
BROKER_USER = ""
BROKER_PASSWORD = ""
BROKER_VHOST = "0"
REDIS_DB = 0
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS = True
CELERY_TASK_RESULT_EXPIRES = 10
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_IMPORTS = ("fetchmyguest.tasks", )
CELERYD_LOG_FILE = os.path.join(PROJECT_DIR, "CELERYD.log")
CELERYBEAT_LOG_FILE = os.path.join(PROJECT_DIR, "CELERYBEAT.log")
CELERY_TRACK_STARTED = True
CELERYD_POOL = 'gevent'

LOGIN_REDIRECT_URL = '/'

# Redis settings
BROKER_URL = "redis://:{password}@{host}:{port}/{db}".format(password=os.getenv('REDIS_PASSWORD', ''),
                                                             host=os.getenv('REDIS_HOST', '127.0.0.1'),
                                                             port=str(os.getenv('REDIS_PORT', '6379')), db=0)

CELERY_RESULT_BACKEND = "redis://:{password}@{host}:{port}/{db}".format(password=os.getenv('REDIS_PASSWORD', ''),
                                                                        host=os.getenv('REDIS_HOST', '127.0.0.1'),
                                                                        port=str(os.getenv('REDIS_PORT', '6379')), db=0)

CACHEOPS_REDIS = {
    'host': 'localhost', # redis-server is on same machine
    'port': 6379, # default redis port
    'db': 1, # SELECT non-default redis database
    # using separate redis db or redis instance
    # is highly recommended
    'socket_timeout': 3,
}

CACHEOPS = {

    'agencies.*': ('all', 60 * 15),
    'leads.*': ('all', 60 * 15),
    'django_mailbox.*': ('all', 60 * 15),

}

# Specifie path to components root (you need to use absolute path)
BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_DIR, 'custom_static/libraries')

BOWER_PATH = '/usr/local/bin/bower'

BOWER_INSTALLED_APPS = (
    'd3#3.3.6',
    'nvd3#1.1.12-beta',
    'codemirror',
    'angular#~1.2.6',
    'json3#~3.2.6',
    'es5-shim#~2.1.0',
    'jquery#~1.10.2',
    # 'bootstrap#~3.0.3',
    'angular-resource#~1.2.6',
    'angular-cookies#~1.2.6',
    'angular-sanitize#~1.2.6',
    'angular-route#~1.2.6',
    'angular-animate#~1.2.6',
    'angular-touch#~1.2.6',
    'angular-bootstrap#0.5.0',
    'angular-ui-select2#~0.0.5',
    'messenger#~1.4.0',
    'underscore#~1.6.0',
    "socket.io-client#~0.9.16",
    "momentjs#~2.5.1",
)

CODEMIRROR_PATH = STATIC_URL + 'codemirror'

# Django Debug Toolbar Settings

AUTO_LOGOUT_DELAY = 600

COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter"
]

COMPRESS_JS_FILTERS = [
    "compressor.filters.jsmin.JSMinFilter"
]


try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

INTERNAL_IPS = ('127.0.0.1',)
djcelery.setup_loader()
