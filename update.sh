#!/bin/sh -e

# @todo output git command to undo (sha hash before git pull)

# Run this on the production server to update code to the latest
# version of the 'production' branch in Git.

git pull

django/manage.py check

#django/manage.py migrate
#django/manage.py migrate -l

make -C django/static/css check
make -C django/static/css
django/manage.py collectstatic --noinput -i \*.less -i Makefile -i todo
(cd htdocs/static/css/ ; ls *.css | egrep -v 'all.css|tinymce.css' | xargs rm)

#django/manage.py collectstatic --noinput
#(cd htdocs/static/css/ ; rm Makefile *.less ; ls *.css | grep -v all.css | xargs rm)
# Note: This will *not* clear out old staticfiles.

touch django/website/wsgi.py
