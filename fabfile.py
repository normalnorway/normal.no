"""
Used to deploy the website.
http://docs.fabfile.org/en/

Note: Production server is on own branch.
"""

import os
from fabric.api import env, local, cd, run, get, put
#from fabric.contrib.console import confirm

env.hosts = ['srv1']
BASE_DIR = '/srv/www/normal.no/'
#BASE_DIR = '/srv/www/dev.normal.no/'
#BRANCH=production


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
        run ('(cd django/static/css/ ; make)')
        # @todo --ignore *.less files
        #run ('django/manage.py collectstatic --noinput')
        run ('touch django/website/wsgi.py')


def bugfix():
    local ('git commit -am bugfix')
    push()
    deploy()



## Database push/pull
# @todo check if changed?

def pushdb():
    '''Copy/push db/normal.db to the server'''
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


# @todo msg as arg
# fab ci my commit message
# fab cip <message> # commit + push
#def commit():
#    local ('git commit')
#def commiti():
#    local ('git add -p')    # interactively add hunks
#    commor()
#
