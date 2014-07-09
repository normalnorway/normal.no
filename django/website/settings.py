# https://docs.djangoproject.com/en/1.5/ref/settings/

from django.conf import global_settings as defaults

# Find full path to Djang's root folder.
import os.path
tmp = os.path.dirname (os.path.abspath (__file__))
tmp = os.path.join (tmp, '..', '..')
ROOT = os.path.normpath (tmp)
#J = lambda filename: os.path.join(ROOT, filename) # todo handle *args
BASE_DIR = ROOT     # @todo ROOT -> BASE_DIR
# @todo BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Private settings that should *not* go inside a public repository!
# Note: Imports ROOT, so must be after that.
import website.settings_local as local


# Only serve website on these hostnames
ALLOWED_HOSTS = (
    'normal.no',
    'www.normal.no',
    'dev.normal.no',    # <-- development site
)
#ALLOWED_HOSTS = ('*',)



##
## Custom settings (not used by Django)
##

# FILE_UPLOAD_MAX_SIZE = "5242880"




##
## Django settings
##

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = local.INTERNAL_IPS

ADMINS = local.ADMINS
MANAGERS = local.MANAGERS

DATABASES = local.DATABASES

SECRET_KEY = local.SECRET_KEY


FILE_UPLOAD_PERMISSIONS = 0644
# FILE_UPLOAD_MAX_MEMORY_SIZE   # 2.5M

# contrib.auth
AUTH_PROFILE_MODULE = 'users.profile'
#LOGIN_URL = '/users/login'
#LOGIN_REDIRECT_URL     # default: /accounts/profile/

TIME_ZONE = 'Europe/Oslo'       # None => /etc/timezone

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'nb-no'
# django.utils.translation.to_locale
# Turns a language name (en-us) into a locale name (en_US).


# contrib.site (required by contrib.flatpages)
SITE_ID = 1

#USE_I18N = False
USE_I18N = True

# Format according to the current locale.
USE_L10N = True
#USE_L10N = False

# UPDATE: USE_I18N=True & LANGUAGE_CODE to format dates!
# TODO but only want date/number formating, not translations! how?

# Use timezone-aware datetimes?
USE_TZ = False

# Absolute filesystem path to store user-uploaded files.
# TODO rename upload?
MEDIA_ROOT = os.path.join (ROOT, 'htdocs', 'media')

# URL of MEDIA_ROOT. Must be mapped by webserver.
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = os.path.join (ROOT, 'htdocs', 'static')

# URL of STATIC_ROOT. Must be mapped by webserver.
STATIC_URL = '/static/'

# Global (non-app) static files.
STATICFILES_DIRS = (
    os.path.join (ROOT, 'django', 'static'),    # static/{css,js,images}
    # TODO split out binary files?
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Templates
TEMPLATE_DIRS = (
    os.path.join (ROOT, 'django', 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # TODO if not DEBUG:
    #   django.template.loaders.cached.Loader
)

#TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.debug',)
#TEMPLATE_CONTEXT_PROCESSORS += defaults.TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS = defaults.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.debug',
)

# @todo remove 'django.core.context_processors.i18n'
#print TEMPLATE_CONTEXT_PROCESSORS


# Note: these are invoked in reverse order for the response.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
        # note: flatpages should be last.
)

# needed for django >= 1.6
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',      # only needed for database-backed session
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    # 'django.contrib.admindocs',

    'core',
    'apps.news',
    'apps.links',
    'apps.content',
    'apps.support',
)


# Sends email to site admins on HTTP 500 error when DEBUG=False.
# http://docs.djangoproject.com/en/dev/topics/logging
#
# @todo
# _LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
# 'level': LOG_LEVEL
# console log that goes to stderr with Errors only?
# Update: if DEBUG: log to console
#         if not DEBUG: log to file
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
        },
        'django.security': {
            'handlers': ['request'],    # @todo mail_admins?
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'request'],
            'level': 'INFO',
            'propagate': False,
        },
    },

    'handlers': {
        'default': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'request': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (BASE_DIR, 'logs', 'request.log'),
            'formatter': 'verbose',
        },
        'security': {
            'class': 'logging.FileHandler',
            'filename': os.path.join (BASE_DIR, 'logs', 'security.log'),
            'formatter': 'verbose',
        },
        # @todo debug.log
    },

    'formatters': {
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
