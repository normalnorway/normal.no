#
# Django settings for normal.no
#
# $ python manage.py diffsettings
#
# TODO
# * DEFAULT_FROM_EMAIL = ikke-svar@normal.no or post@normal.no
# * Session timeout
# * Crontab to periodically clean session database
#

BASE_DIR = None # Not in use, but keeps Django happy (avoids 1_6.W001).
# SILENCED_SYSTEM_CHECKS = ['1_6.W001']

import os
from django.conf import global_settings as defaults

def rootdir (*args):    # rename mk_filename
    """Constructs a path relative to the project root directory"""
    return os.path.join (rootdir.base, *args)
rootdir.base = reduce(lambda n,f: f(n), [__file__] + 3*[os.path.dirname]) # calls os.path.dirname 3 times on __file__ recursively
# Q: Are these two always equal? __file__ == os.path.normpath(__file__)
# If not, use normpath instead of __file__ ?
# A: lets check
assert __file__ == os.path.normpath(__file__)



DEBUG = not os.path.exists (rootdir ('NODEBUG'))
TEMPLATE_DEBUG = DEBUG

# Admins will get email whenever an error happens (and DEBUG=False).
ADMINS = (
     ('Torkel', 'torkel@normal.no'),
)

# Managers will get broken-link notification.
# But only when BrokenLinkEmailsMiddleware is active.
MANAGERS = ADMINS


# Only serve website on these hostnames. Only active when DEBUG=False.
ALLOWED_HOSTS = (
    'normal.no',
    #'www.normal.no',   # Note: Apache redirects www.normal.no => normal.no
    'dev.normal.no',    # <-- development site
    'normal.i2p',       # I2P address
    'qrw3w45sx7niqcpg.onion',   # Tor address
)
#ALLOWED_HOSTS = ('*',)


# Note: Default is '/accounts/login/'.
# Also accepts view function names and named URL patterns
LOGIN_URL = '/admin/login/'
#LOGOUT_URL = '/admin/logout/'
#PASSWORD_RESET_TIMEOUT_DAYS = 3


# Note: django.core.context_processors.debug is only active when
# request.META['REMOTE_ADDR']) is in INTERNAL_IPS.
# So put your client ip-address here for debugging.
INTERNAL_IPS = ['127.0.0.1']
# @todo only if DEBUG ?

# @todo join all if DEBUG sections?
#if DEBUG:
#    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


# contrib.site (required by contrib.flatpages)
SITE_ID = 1


## Localization
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'nb-no'
USE_I18N = True     # translate messages
USE_L10N = True     # format according to the current locale (LANGUAGE_CODE)

TIME_ZONE = 'Europe/Oslo'
USE_TZ = False


## Static and media files

STATICFILES_DIRS = (
    rootdir ('django', 'static'),
)

STATIC_ROOT = rootdir ('htdocs', 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = rootdir ('htdocs', 'media')
MEDIA_URL = '/media/'


# Default
#STATICFILES_FINDERS = (
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder', # not used
#)


## Templates
TEMPLATE_DIRS = (
    rootdir ('django', 'templates'),
)

# Only used by dev-site to check if request.META.SERVER_NAME == dev.normal.no
# So might be better to use own context processor for this.
TEMPLATE_CONTEXT_PROCESSORS = defaults.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

# This is the default
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',   # not used
#)
#if not DEBUG:
#    TEMPLATE_LOADERS = (('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),)
if not DEBUG:   # Enable template caching on the production site.
    TEMPLATE_LOADERS = (('django.template.loaders.cached.Loader', defaults.TEMPLATE_LOADERS),)


## Applications, etc.

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',      # only needed for database-backed session
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',         # @todo remove
    'django.contrib.flatpages',     # @todo remove

    # Local apps
    'core',
    'tinymce4',     # only to get staticfiles
    'apps.news',
    'apps.links',
    'apps.content',
    'apps.support',
)


# Note: these are invoked in reverse order for the response.
MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware', # 1.7
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware', # Note: must be last!
]
import django
if django.VERSION[0:2] < (1,7):
    MIDDLEWARE_CLASSES.remove ('django.contrib.auth.middleware.SessionAuthenticationMiddleware')


# manage.py dumpdata [app...] --indent 2 --database dev
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME':     rootdir ('db', 'normal.db'),
        'CONN_MAX_AGE': 0 if DEBUG else 3600
    },
    'mysql': {
        'ENGINE':   'django.db.backends.mysql',
        "HOST":     '/var/run/mysql',
        'NAME':     'normalno',
        'USER':     'normalno',
        #'PASSWORD': inifile.get ('database', 'password', ''),
        #'OPTIONS':  { 'read_default_file': '/path/to/my.cnf' },
        # https://docs.djangoproject.com/en/1.7/ref/databases/#connecting-to-the-database
        # Remember: CREATE DATABASE <dbname> CHARACTER SET utf8;
        # Remember: INODB
        # @todo make mysql default and rename sqlite -> dev? then don't need conn_max_age hack
    },
}
# Update: Will get error if host is missing mysql backend, even if it's
# not used. Therefore must add conditionally.
if DEBUG: del DATABASES['mysql']

#if not DEBUG:
#    DATABASES['default']['CONN_MAX_AGE'] = 3600
# Enable persistent db connections.
# Note: Sometimes a database won't be accessed by the majority of your
# views, for example because it's the database of an external system, or
# thanks to caching. In such cases, you should set CONN_MAX_AGE to a low
# value or even 0, because it doesn't make sense to maintain a connection
# that's unlikely to be reused.


CACHES = {
    'default': { # This is a thread-safe, per-process cache.
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 3600
    }
    #'dev': { DummyCache. And select if DEBUG }
}
if DEBUG:
    CACHES['default'] = { # Dummy caching for development
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }


ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'


# Note: The secret key must be the same for all processes and not change
# between sessions. It can therefore only be auto-generated once, and must
# then be written to persistent storage and loaded on each subsequent run.
if DEBUG:
    SECRET_KEY = 'x' * 50
    #SECRET_KEY = ''.join (chr(random.randint(33,126)) for x in xrange(50))
else:
    try:
        SECRET_KEY = open (rootdir('secret-key')).readline()
    except IOError, ex:
        import sys, base64
        key = base64.b64encode (os.urandom(48))
        print >>sys.stderr, 'ERROR: %s: %s' % (ex.filename, ex.strerror)
        print >>sys.stderr, 'You can create it like this:'
        print >>sys.stderr, 'echo %s > %s' % (key, ex.filename)
        os.abort()



## Logging
# Sends email to site admins on HTTP 500 error when DEBUG=False.
# http://docs.djangoproject.com/en/dev/topics/logging
#
# Testing things out, so more complex than it should be.
#
# @todo if DEBUG log to console (or debug.log)
#       or only level=>errors to console/stderr, and rest to debug.log?
#       or if DEBUG: log to console else: log to file
# @todo catch all level=ERROR into own file? (apache uses error.log)

# _LEVEL = 'DEBUG' if DEBUG else 'WARNING'
# LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
#logfile = lambda f: os.path.join (ROOT_DIR, 'logs', f)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True, # @todo keep djangos default logging
                                      # q: how to see 'em?
                                      # a: https://docs.djangoproject.com/en/1.7/topics/logging/#default-logging-configuration

    'loggers': {
        # @todo can drop handler and get default?
        # Q: what is default level. move level to handlers?
        # @todo drop?
        '': {
            'handlers': ['file:website'],
            'level': 'DEBUG',
        },

        'apps': {
            'handlers': ['console'],
            'propagate': True,
            # @todo also log to apps.log, then disable propagate
            # or better to just propagate to website.log?
        },


        ## django.* loggers

        # Catch-all logger. No messages are posted directly to this logger.
        'django': {
            'handlers': ['file:django'],
            'level': 'DEBUG',
        },

        # django.db.backends
        # Every application-level SQL statement executed by a request is
        # logged at the DEBUG level.
        # Extra context: duration, sql, params
        #
        # django.db.backends.schema     create, insert, drop, alter, etc
        # django.db.backends            query log

#        'django.db.backends.schema': {
#            'handlers': ['file:database'],  # querylog (changes)
#            'level': 'DEBUG',
#        },
#        'django.db.backends': {
#            'handlers': ['file:sql'],       # querylog (select)
#            'level': 'DEBUG',
#        },
        # @todo still wan't INFO+ messages logged to django.log
        #       or website.log. fix: pass to multiple handlers
        #       with diferent level

        # django.security.*
        # Messages on any occurrence of SuspiciousOperation. There is
        # a sub-logger for each sub-type of SuspiciousOperation.
        # Most occurrences are logged as a warning, while any
        # SuspiciousOperation that reaches the WSGI handler will be
        # logged as an error.
        # The django.security logger is configured the same as the request
        # logger, and any error events will be mailed to admins.
        'django.security': {
            'handlers': ['file:security', 'mail_admins'],
            'level': 'DEBUG',
            #'propagate': True, # or also log to website.log
        },

        # 5XX responses are raised as ERROR messages
        # 4XX responses are raised as WARNING messages
        # Extra context: status_code, request
        #   q: howto use em? custom formatter?
        'django.request': {
            'handlers': ['file:request', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        }, # @todo possible to filter out Not found? they are ~98%
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['debug_false'],
            # Attach the full content of the debug Web page that would
            # have been produced if DEBUG were True.
            # Note: contains a full traceback; potentially very sensitive
            'include_html': True,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default', # note: this is not the default
            # 'stream': sys.stdout, # default is stderr
            #'formatter': 'verbose',
        },
        'file:website': {
            #'level': _LEVEL?
            'class': 'logging.FileHandler',
            'filename': rootdir ('logs', 'website.log'),
            'formatter': 'verbose',
        },
        'file:django': {
            'class': 'logging.FileHandler',
            'filename': rootdir ('logs', 'django.log'),
            'formatter': 'verbose',
        },
        'file:request': {
            'class': 'logging.FileHandler',
            'filename': rootdir ('logs', 'request.log'),
            'formatter': 'verbose',
        },
        'file:security': {
            'class': 'logging.FileHandler',
            'filename': rootdir ('logs', 'security.log'),
            'formatter': 'verbose',
        },
        # @todo catch all level>=ERROR into error.log
        # @todo does RotatingFileHandler exists?
        # @todo can drop formatter on handlers (and get default)?
    },

    'formatters': {
        # q: howto define default? '' a: not possible
        # @todo drop %(lineno) for everything except own code (apps, core?)
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'default': {
            'format': '%(levelname)s: %(message)s'
        },
    },

    'filters': {
        'debug_false': {    # nodebug?
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
}
