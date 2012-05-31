# Django settings for normal.no
# @todo vim folding of sections (and TOC?)

# Do this to get access to these settings:
# from django.conf import settings
# settings.FAVORITE_COLOR

# Settings used by django
# DEFAULT_FROM_EMAIL    # Default: 'webmaster@localhost'

# Custom settings
# MAX_UPLOAD_SIZE = "5242880"?

# NEW
AUTH_PROFILE_MODULE = 'apps.users.Profile'
#LOGIN_URL = '/users/login'
#LOGIN_REDIRECT_URL     # default: /accounts/profile/

#LOGIN_URL = '/admin/login'
  # can not use this, since /admin/ already requires auth



DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('torkel', 'torkel@normal.no'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'normal',   # Or path to database file if using sqlite3.
        'USER': 'normal',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# A value of None will use system settings (/etc/timezone)
# system time zone.
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# For "sites" framework? Only have one site, but the flatpages app
# requires it.
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True




##
## MEDIA & STATIC FILES
##

# Q: ADMIN_MEDIA_PREFIX = '/media/admin/'

# Absolute filesystem path to store user-uploaded files.
MEDIA_ROOT = '/srv/www/normal.no/upload/'
  # q: rename media-root or media?

# URL that handles the media served from MEDIA_ROOT (need trailing slash).
MEDIA_URL = '/media/'
  # @note must be mapped by webserver. how?
  # @note Django does not serve MEDIA_ROOT by default.
  #       @see http://stackoverflow.com/a/8542030


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = '/srv/www/normal.no/htdocs'
  # q: rename static-root?

# URL prefix for static files.
# Example: "http://example.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files (must be absolute path).
STATICFILES_DIRS = (
    '/srv/www/normal.no/django/static',
    # @todo add path for non-code static files? (split code and media)
    # Now code lives in:  static/css/ & static/js/
    # And media lives in: static/images/
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)




##
## OTHER
##

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'd%3luowws4k+77pe&amp;d@mkd7qx_-x$!c(jvs(9ah_-i92o9d8en'


# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (
    '/srv/www/normal.no/django/templates',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.eggs.Loader',
)
# django.template.loaders.cached.Loader
# By default, the templating system will read and compile your templates
# every time they need to be rendered.


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Note: flatpages should be last.
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'normal.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'normal.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # Custom apps
    'apps.files',
    'apps.images',
    'apps.users',
    'apps.news',
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
