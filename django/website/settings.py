#
# Django settings for normal.no
#
# $ python manage.py diffsettings
#
# TODO
# DEFAULT_FROM_EMAIL = ikke-svar@normal.no
# increase cache timeout? TIMEOUT = 300
# enable persistent db connections? CONN_MAX_AGE = 0
#

from django.conf import global_settings as defaults

import os
BASE_DIR = os.path.dirname (os.path.dirname (__file__))
ROOT_DIR = os.path.dirname (BASE_DIR)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Admins will get email whenever an error happens and DEBUG=False.
ADMINS = (
     ('Torkel', 'torkel@normal.no'),
)

# Managers will get broken-link notification.
# But only when BrokenLinkEmailsMiddleware is active.
MANAGERS = ADMINS


# Only serve website on these hostnames. Only active when DEBUG=False.
ALLOWED_HOSTS = (
    'normal.no',
    'www.normal.no',
    'dev.normal.no',
)

# Note: django.core.context_processors.debug is only active when
# request.META['REMOTE_ADDR']) is in INTERNAL_IPS.
# So put your client ip-address here for debugging.
INTERNAL_IPS = ['127.0.0.1']
if DEBUG:
    INTERNAL_IPS += ('176.58.124.187', '2a01:7e00::f03c:91ff:feae:a668')


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
    os.path.join (BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join (ROOT_DIR, 'htdocs', 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join (ROOT_DIR, 'htdocs', 'media')
MEDIA_URL = '/media/'


# Default
#STATICFILES_FINDERS = (
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder', # not used
#)


## Templates
TEMPLATE_DIRS = (
    os.path.join (BASE_DIR, 'templates'),
)

#TEMPLATE_CONTEXT_PROCESSORS = defaults.TEMPLATE_CONTEXT_PROCESSORS + (
#    'django.core.context_processors.request',
#)

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
    'apps.news',
    'apps.links',
    'apps.content',
    'apps.support',
)


# Note: these are invoked in reverse order for the response.
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware', # Note: must be last!
)

ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'

# needed for django >= 1.6
# Note: not needed on inormal. why?
#TEST_RUNNER = 'django.test.runner.DiscoverRunner'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join (ROOT_DIR, 'db', 'normal.db'),
    }
}


if DEBUG:
    SECRET_KEY = 'this is not very secret; it is used for debugging!'
else:
    try:
        SECRET_KEY = open (os.path.join(ROOT_DIR, 'secret-key')).readline()
    except IOError:
        # @todo create secret-key file?
        print 'Warning: "secret-key" file not found! Using temporary key instead!'
        from base64 import b64encode
        SECRET_KEY = b64encode(os.urandom(48))
        #import random
        #SECRET_KEY = ''.join (chr(random.randint(33,126)) for x in xrange(54))


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
#logfile = lambda f: os.path.join (ROOT_DIR, 'logs', f)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'loggers': {
        # @todo can drop handler and get default?
        # Q: what is default level. move level to handlers?
        '': {
            'handlers': ['file:website'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['file:django'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['file:security', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file:request', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['debug_false'],
            'include_html': True,
        },
        'file:website': {
            #'level': _LEVEL?
            'class': 'logging.FileHandler',
            'filename': os.path.join (ROOT_DIR, 'logs', 'website.log'),
            'formatter': 'verbose',
        },
        'file:django': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (ROOT_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'file:request': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (ROOT_DIR, 'logs', 'request.log'),
            'formatter': 'verbose',
        },
        'file:security': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (ROOT_DIR, 'logs', 'security.log'),
            'formatter': 'verbose',
        },
        # @todo can drop formatter on handlers (and get default)?
        # @todo debug.log?
    },

    'formatters': {
        # @todo drop %(lineno) for django; only usefull for own code
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'default': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'filters': {
        'debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
}
