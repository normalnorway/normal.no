"""
Used to deploy the website (and other tasks).
http://docs.fabfile.org/en/

Note: Production server is on own branch.
"""

import os
from fabric.api import env, local, lcd, cd, run, get, put
from fabric.api import settings
from fabric.contrib.console import confirm

env.hosts = ['srv1']
BASE_DIR = '/srv/www/normal.no/'
#BASE_DIR = '/srv/www/dev.normal.no/'
# @todo -d switch to deploy on staging server (or can use host=dev?)


def test():
    '''Run all unit tests'''
    with lcd ('django'):
        local ('./manage.py test')


def livetest():
    '''Check that the live site is working'''
    with settings(warn_only=True):  # don't abort if test fail
        r = local ('python test/livetest.py')
        return r.succeeded



# 1) test first
# 2) deploy (tag, merge)
# 3) livetest
#    ok: remove tag
#    fail: roll back to tag
# @todo don't do collectstatic by default, move that to: deploy-full
def deploy():
    push()
    with cd (BASE_DIR):
        #run ('git pull')
        #run ('git checkout ' + BRANCH) # for safety?
#        with cd ('django/static/css'):
#            run ('make')
        run ('git fetch -q')
        run ('git merge origin/master')
        #run ('(cd django/static/css/ ; make)')
        # @todo --ignore *.less files
        #run ('django/manage.py collectstatic --noinput')
        run ('touch django/website/wsgi.py')


def staticfiles():
    with cd (BASE_DIR):
        with cd ('django/static/css'): run('make')
        run (r'django/manage.py collectstatic --noinput -i \*.less -i Makefile')
        # @todo ignore everythin except all.css?


#def bugfix():
#    local ('git commit -am bugfix')
#    push()
#    deploy()



## Database push/pull

# Danger, danger!

def pushdb():
    '''Copy/push db/normal.db to the server'''
    ok = confirm ('WARNING: Will replace live data on normal.no', False)
    if not ok: return
    with cd (BASE_DIR):
        # Note: using cp instead of mv to preserve permissions
        run ('cp db/normal.db db/normal.db-$(date +%m%d%H%M)')
        put ('db/normal.db', 'db/normal.db')


def pulldb():
    '''Copy/pull db/normal.db from the server'''
    local ('mv db/normal.db db/normal.db-$(date +%m%d%H%M)')
    get (os.path.join (BASE_DIR,'db','normal.db'), 'db/normal.db')



## Base git commands
def push():
    local ('git push')
