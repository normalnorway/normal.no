"""
Used to deploy the website.
http://docs.fabfile.org/en/

TODO:
- compile less
- ./manage.py collectstatic
- Run on own production branch? BRANCH=production
"""

from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm

BASE_DIR = '/srv/www/dev.normal.no/'


def deploy():
    with cd (BASE_DIR):
        run ('git pull')
        #run ('git fetch')
        #run ('git merge master')
        run ('touch django/website/wsgi.py')


def bugfix():
    local ('git commit -am bugfux')
    push()
    deploy()


def push():
    local ('git push')


#def commit():
#    #local ('git add -p')   # interactively add hunks
#    local ('git commit')
