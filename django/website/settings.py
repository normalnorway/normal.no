# https://docs.djangoproject.com/en/1.4/ref/settings/


##
## Custom settings (not used by Django)
##
ROOT = '/srv/www/new.normal.no/'

# FILE_UPLOAD_MAX_SIZE = "5242880"



##
## Django settings
##

DEBUG = True
TEMPLATE_DEBUG = DEBUG


# Admins will get email whenever an error happens.
# Managers will get broken-link notification.
ADMINS = (
    ('torkel', 'torkel@normal.no'),
)
MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ROOT + 'django/normal.db',
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'normal',
#        'USER': 'normal',
    }
}


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'd%3luowws4k+77pe&amp;d@mkd7qx_-x$!c(jvs(9ah_-i92o9d8en'


FILE_UPLOAD_PERMISSIONS = 0644
# FILE_UPLOAD_MAX_MEMORY_SIZE   # 2.5M

# contrib.auth
AUTH_PROFILE_MODULE = 'users.profile'
#LOGIN_URL = '/users/login'
#LOGIN_REDIRECT_URL     # default: /accounts/profile/

TIME_ZONE = 'Europe/Oslo'       # None => /etc/timezone

LANGUAGE_CODE = 'en-us'

# contrib.site (required by contrib.flatpages)
SITE_ID = 1

USE_I18N = False

# Format according to the current locale.
USE_L10N = False

# Use timezone-aware datetimes?
USE_TZ = False



# Absolute filesystem path to store user-uploaded files.
# @todo rename upload?
MEDIA_ROOT = ROOT + 'htdocs/media/'

# URL of MEDIA_ROOT. Must be mapped by webserver.
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = ROOT + 'htdocs/static/'

# URL of STATIC_ROOT. Must be mapped by webserver.
STATIC_URL = '/static/'

# Global (non-app) static files.
STATICFILES_DIRS = (
    ROOT + 'django/static',     # static/{css,js,images}
    # @todo split out binary files?
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)



TEMPLATE_DIRS = (
    ROOT + '/django/templates',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # @todo if not DEBUG:
    #   django.template.loaders.cached.Loader
)


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


ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'website.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    # 'django.contrib.admindocs',

    'apps.news',
    'apps.links',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
