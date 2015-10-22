# coding: utf8
#
# Displays differences between current settings and Django's default:
# $ python manage.py diffsettings
#

# SESSION_COOKIE_AGE                        # default is 2 weeks
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True    # default is False

from django.conf import global_settings as defaults

import os
BASE_DIR = os.path.dirname (os.path.dirname (__file__))

from .siteconfig import SiteConfig
Config = SiteConfig (os.path.join (BASE_DIR, os.path.pardir, 'site.ini'))

# Add piwiki visitor tracking javascript code
# @todo prefix with SITE_?
PIWIKI = Config.getbool ('main.piwiki', False)

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

# Testing. Note: Will affect both admin and template
USE_L10N = False
DATETIME_FORMAT = r'j. F Y, k\l. H:i'
DATE_FORMAT = 'j. F Y'  # some news articles don't have time

# Testing. Only use english. Update: Worked fine, except for english month
# names on the public part. @todo try to change locale of wsgi process
#USE_I18N = False


DEBUG = Config.getbool ('main.debug', True)

INTERNAL_IPS = ['127.0.0.1']
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

    'core',         # needed?
    'tinymce4',     # only used to get staticfiles
    'apps.news',
    'apps.links',
    'apps.support',
    'apps.polls',
    'apps.erp.apps.ErpAppConfig',
    'apps.cms.apps.CmsAppConfig',
)


# manage.py dumpdata [app...] --indent 2 --database sqlite
_DATABASES = {
    'sqlite': {     # development backend
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join (BASE_DIR, 'db.sqlite3'),
    },
    'mysql': {      # production backend
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     Config.get ('database.name', ''),
        'USER':     Config.get ('database.user', ''),
        'PASSWORD': Config.get ('database.password', ''),
        'CONN_MAX_AGE': 3600,
    },
}
DATABASES = {
    'default': _DATABASES[Config.get('database.backend','sqlite')]
}


## Cache
CACHES = {
    'default': { # This is a thread-safe, per-process cache.
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 3600,    # default ttl?
    }
}
if DEBUG: CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
}


## Templates
_loaders = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
if not DEBUG:   # Enable template caching
    _loaders = [('django.template.loaders.cached.Loader', _loaders)]

# https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/
# If it sets TEMPLATE_DEBUG to a value that differs from DEBUG, include
# that value under the 'debug' key in 'OPTIONS'.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join (BASE_DIR, 'templates') ],
        'OPTIONS': {
            #'debug': True, # default if DEBUG=True
            'loaders': _loaders,
            'context_processors': defaults.TEMPLATE_CONTEXT_PROCESSORS + (
                'django.template.context_processors.request', # needed?
                'core.context_processors.siteconfig',
            ),
        },
    },
]
del _loaders
#TEMPLATES[0]['OPTIONS']['string_if_invalid'] = '{{NULL}}',


## Static & media files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join (BASE_DIR, 'static'),
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join (BASE_DIR, '..', 'htdocs', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join (BASE_DIR, '..', 'htdocs', 'media')


# Note: these are invoked in reverse order for the response.
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # https://docs.djangoproject.com/en/1.8/ref/settings/#secure-browser-xss-filter
    #'django.middleware.security.SecurityMiddleware',
)


ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


# Note: The secret key must be the same for all processes and not change
# between sessions. It can therefore only be auto-generated once, and must
# then be written to persistent storage and loaded on each subsequent run.
SECRET_KEY = Config.get ('main.secret', 'x' * 50)

if not DEBUG and SECRET_KEY == 'x'*50:
    import sys, base64
    key = base64.b64encode (os.urandom(48))
    print >>sys.stderr, 'This looks like a production system and the default SECRET_KEY is weak!'
    print >>sys.stderr, 'Please insert this as main.secret in site.ini:\n' + key
    os.abort()


## Logging

# Note: Different logging setup for debug/dev than for production.
# DEBUG: Logs everything with level >= INFO to the console
# LIVE:  Log to files in django/logs/*.log

_LOGGING_DEBUG = {
    'version': 1,

    'loggers': {
        '': {   # catch-all
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'formatters': {
        'simple': { 'format': '%(levelname)s %(message)s' },
    },
}

# @todo also log warnings in catch-all logger?
_LEVEL = 'INFO'
_LOGGING_LIVE = {
    'version': 1,
    #'disable_existing_loggers': False,

    # @todo need catch-all logger at warning level? warnings.log
    # @todo catch-all.log on srv1 no longer in use
    'loggers':
    {
        '': {
            'handlers': ['file:error'],
            'level': 'ERROR',
        },
        'apps': {
            'handlers': ['file:apps', 'file:error'],
            'level': _LEVEL,
            'propagate': False,
        },
        'django': {
            'handlers': ['file:django', 'file:error'],
            'level': _LEVEL,
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file:security', 'file:error'],
            'level': _LEVEL,
            'propagate': False,
        },
        'django.request': {
            #'handlers': ['file:request', 'file:error'],
            'handlers': ['file:request', 'file:error', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },  # @todo possible to filter out Not found? they are ~98%
    },

    'handlers':
    {
        'file:error': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'filename': os.path.join (BASE_DIR, 'logs', 'error.log'),
            'formatter': 'verbose',
        },
        'file:apps': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (BASE_DIR, 'logs', 'apps.log'),
            'formatter': 'apps',
        },
        'file:django': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'file:request': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (BASE_DIR, 'logs', 'request.log'),
            'formatter': 'verbose',
        },
        'file:security': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (BASE_DIR, 'logs', 'security.log'),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },

    # https://docs.python.org/2/library/logging.html#logrecord-attributes
    'formatters': {
        'verbose': {
            'format' : "%(asctime)s %(levelname)s [%(name)s] : %(message)s",
            'datefmt' : "%Y-%m-%d %H:%M:%S",
        },
        'apps': { # like verbose but add function name
            'format' : "%(asctime)s %(levelname)s [%(name)s:%(funcName)s] : %(message)s",
            'datefmt' : "%Y-%m-%d %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
}

LOGGING = _LOGGING_DEBUG if DEBUG else _LOGGING_LIVE
if DEBUG:
    del _LOGGING_LIVE
else:
    del _LOGGING_DEBUG


del Config  # release memory
