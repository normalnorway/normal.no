"""
Not in use!

@todo task to deploy on production server and rollback if livetest fails
@todo task to deploy to staging server
"""

import os
from fabric.api import env, local, lcd, cd, run, get, put
from fabric.api import settings
#from fabric.contrib.console import confirm

env.hosts = ['normal.no']
BASE_DIR = '/srv/www/normal.no/'


def test():
    '''Run all unit tests'''
    with lcd ('django'):
        local ('./manage.py test')


def livetest():
    '''Check that the live site is working'''
    with settings(warn_only=True):  # don't abort if test fail
        r = local ('python test/livetest.py')
        return r.succeeded


def staticfiles():
    '''Create (less -> css) and collect static files'''
    with cd (BASE_DIR):
        with cd ('django/static/css'):
            run('make')
        run (r'django/manage.py collectstatic --noinput -i \*.less -i Makefile')
