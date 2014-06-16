"""
Used to deploy the website.
http://docs.fabfile.org/en/

Note: Production server is on own branch.
"""

from fabric.api import local, run, cd, env
from fabric.contrib.console import confirm

env.hosts = ['srv1']
BASE_DIR = '/srv/www/dev.normal.no/'
#BRANCH=production


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
        run ('django/manage.py collectstatic --noinput')
        run ('touch django/website/wsgi.py')


def bugfix():
    local ('git commit -am bugfix')
    push()
    deploy()



## Base git commands
def push():
    local ('git push')

# @todo msg as arg
#def commit():
#    local ('git commit')
#def commiti():
#    local ('git add -p')    # interactively add hunks
#    commor()
