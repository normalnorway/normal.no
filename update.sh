#!/bin/sh -e

# Run this on the production server to update code to the latest
# version of the 'production' branch in Git.

git pull
git submodule update

make -C django/static/css
django/manage.py collectstatic --noinput -i \*.less -i Makefile
(cd htdocs/static/css/ ; ls *.css | egrep -v 'all.css|tinymce.css' | xargs rm)

#django/manage.py collectstatic --noinput
#(cd htdocs/static/css/ ; rm Makefile *.less ; ls *.css | grep -v all.css | xargs rm)
# Note: This will *not* clear out old staticfiles.

# django/manage.py check

touch django/website/wsgi.py
