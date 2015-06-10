# coding: utf8
#
# Displays differences between current settings and Django's default:
# $ python manage.py diffsettings
#

import os
from django.conf import global_settings as defaults

BASE_DIR = os.path.realpath (os.path.join (__file__, '../../../'))

def rootdir (*args):    # rename mk_filename
    """Constructs a path relative to the project root directory"""
    return os.path.join (BASE_DIR, *args)

from siteconfig import SiteConfig
Config = SiteConfig (rootdir ('site.ini'))


DEFAULT_FROM_EMAIL = 'post@normal.no'

LOGIN_URL = '/admin/login/'
#LOGOUT_URL = 'admin:logout'   # supports named urls


# Admins will get email whenever an error happens
# Managers will get broken-link notification
ADMINS = (
     ('Torkel', 'torkel@normal.no'),
)
MANAGERS = ADMINS


# Localization
LANGUAGE_CODE = 'nb-no'
TIME_ZONE = 'Europe/Oslo'
USE_I18N = True     # translate messages
USE_L10N = True     # format according to the current locale (LANGUAGE_CODE)
USE_TZ = False

# Note: These are not active when USE_L10N is True
# Q: howto change these without own: locale/nb/formats.py ?
#DATE_FORMAT = 'j. F Y'
#TIME_FORMAT = 'H:i'
#DATETIME_FORMAT = DATE_FORMAT + ', k\l. ' + TIME_FORMAT


#DEBUG = not os.path.exists (rootdir ('NODEBUG'))
DEBUG = Config.getbool ('main.debug', True)
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ['127.0.0.1']    # needed for what? A: debug in templates
#INTERNAL_IPS = ['127.0.0.1', '::1']


# Only serve website on these hostnames
# Note: Apache redirects www.normal.no => normal.no
ALLOWED_HOSTS = (
    'normal.no',
    'normal.i2p',               # I2P address
    'qrw3w45sx7niqcpg.onion',   # Tor address
    'dev.normal.no',
    'test.normal.no',           # staging server
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',      # only needed for database-backed session
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',         # flatpages dependence
    'django.contrib.flatpages',

    'core',
    'tinymce4',     # only used to get staticfiles
    'apps.news',
    'apps.links',
    'apps.content',
    'apps.support',
)


# manage.py dumpdata [app...] --indent 2 --database dev
DATABASES = {
    'dev': {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME':     rootdir ('db', 'normal.db'),
    },
    'mysql': {
        'ENGINE':   'django.db.backends.mysql',
        #'HOST':     '/var/run/mysqld/mysqld.sock',     # default
        #'HOST':            Config.get ('database.hostname'),
        'NAME':     Config.get ('database.name', ''),
        'USER':     Config.get ('database.user', ''),
        'PASSWORD': Config.get ('database.password', ''),
        #'CONN_MAX_AGE': 3600,
        #'CONN_MAX_AGE': 0 if DEBUG else 3600
        #'OPTIONS':  { 'read_default_file': '/path/to/my.cnf' },
        # https://docs.djangoproject.com/en/1.7/ref/databases/#connecting-to-the-database
        # Remember: CREATE DATABASE <dbname> CHARACTER SET utf8;
        # Note: Django don't create INODB tables by default!
        # UPDATE: Did create INODB by default now (Django 1.8)
        # But does not use utf8 by default!
    },
}
DATABASES['default'] = DATABASES['dev' if DEBUG else 'mysql']
del DATABASES['dev']
del DATABASES['mysql']

#del DATABASES['dev' if not DEBUG else 'mysql']
#if DEBUG: del DATABASES['mysql']
#DATABASES['default'] = DATABASES['mysql']
#DATABASES['default'] = DATABASES[Config.get('dbengine', 'dev')]



CACHES = {
    'default': { # This is a thread-safe, per-process cache.
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 3600
    }
}
if DEBUG: CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
}


## Templates
TEMPLATE_DIRS = (
    rootdir ('django', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = defaults.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)   # Note: Only used by dev-site to check request.META.SERVER_NAME

if not DEBUG:   # Enable template caching on the production site.
    TEMPLATE_LOADERS = (('django.template.loaders.cached.Loader', defaults.TEMPLATE_LOADERS),)


## Static & media files
STATICFILES_DIRS = (
    rootdir ('django', 'static'),
)

STATIC_URL = '/static/'
STATIC_ROOT = rootdir ('htdocs', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = rootdir ('htdocs', 'media')


# Note: these are invoked in reverse order for the response.
MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware', # Note: must be last!
]


ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'

# contrib.site (required by contrib.flatpages)
SITE_ID = 1

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


# Note: The secret key must be the same for all processes and not change
# between sessions. It can therefore only be auto-generated once, and must
# then be written to persistent storage and loaded on each subsequent run.
SECRET_KEY = Config.get ('main.secret', 'x' * 50)
# @todo fail if missing!

if not DEBUG and SECRET_KEY == 'x'*50:
    import sys, base64
    key = base64.b64encode (os.urandom(48))
    print >>sys.stderr, 'This looks like a production system and the default SECRET_KEY is weak!'
    print >>sys.stderr, 'Please insert this as main.secret in site.ini:\n' + key
    os.abort()


## Logging

# By default, Django configures the django.request logger so that all
# messages with ERROR or CRITICAL level are sent to AdminEmailHandler, as
# long as the DEBUG setting is set to False.

_LEVEL = 'DEBUG' if DEBUG else 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers':
    {
        '': {
            'handlers': ['file:catch-all', 'console'],
            'level': _LEVEL,
        },

        # @todo catch all level>=ERROR into errors.log?
        # Q: Howto log all errors into errors.log?
        #    can not remove propagate:False bellow
        #    handlers += 'file:error' and filter on that handler

        'apps': {
            'handlers': ['file:apps', 'console'],
            'level': _LEVEL,
            'propagate': False,
        },

        'django': {
            'handlers': ['file:django', 'console'],
            'level': _LEVEL,
            'propagate': False,
        },

        'django.db.backends': {
            'handlers': ['file:db'],
            'level': 'INFO',    # don't log all sql queries
            'propagate': False,
        },
        'django.db.backends.schema': {
            'handlers': ['file:db'],
            'level': 'DEBUG',   # log sql that modifies the schema
            'propagate': False,
        },

        'django.security': {
            'handlers': ['file:security'],
            'level': _LEVEL,
            'propagate': False,
        },

        'django.request': {
            'handlers': ['file:request'],
            'level': 'INFO',    # all request are logged at DEBUG
            'propagate': False,
        }, # @todo possible to filter out Not found? they are ~98%
    },


    'handlers':
    {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG', # is this the default?
            'formatter': 'simple',
            'filters': ['debug'],
        },

#        'null': {
#            'class': 'logging.NullHandler',
#        },

        'file:catch-all': {
            'class': 'logging.FileHandler',
            'filename': rootdir ('django', 'logs', 'catch-all.log'),
            'formatter': 'verbose',
        },

        'file:apps': {
            'class': 'logging.FileHandler',
            'filename': rootdir ('django', 'logs', 'apps.log'),
            'formatter': 'verbose',
        },

        'file:django': {
            'class': 'logging.FileHandler',
            'filename': rootdir ('django', 'logs', 'django.log'),
            'formatter': 'verbose',
        },

        'file:db': {
            'class': 'logging.FileHandler',
            'filename': rootdir ('django', 'logs', 'db.log'),
            'formatter': 'verbose',
        },

        'file:request': {
            'class': 'logging.FileHandler',
            'filename': rootdir ('django', 'logs', 'request.log'),
            'formatter': 'verbose',
        },

        'file:security': {
            'class': 'logging.FileHandler',
            'filename': rootdir ('django', 'logs', 'security.log'),
            'formatter': 'verbose',
        },

#        'file:error': {
#            'level': 'ERROR',
#            'class': 'logging.FileHandler',
#            'formatter': 'verbose',
#            'filename': rootdir ('django', 'logs', 'error.log'),
#        },
    },


    # https://docs.python.org/2/library/logging.html#logrecord-attributes
    'formatters': {
        'verbose': {
            'format' : "%(asctime)s %(levelname)s [%(name)s] : %(message)s",
            'datefmt' : "%Y-%m-%d %H:%M:%S",
        },
#        'custom': {
#            # Like verbose, but add function name. Only use for own code (apps.)
#            'format' : "%(asctime)s %(levelname)s [%(name)s:%(funcName)s] : %(message)s",
#            'datefmt' : "%Y-%m-%d %H:%M:%S",
#        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'filters': {
        'debug': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
#        'nodebug': {
#            '()': 'django.utils.log.RequireDebugFalse'
#        },
    },
}
