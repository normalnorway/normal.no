#!/bin/sh -e

# Run this on the production server to update the code

echo -n Last god commit
git rev-parse master

git pull

sh mkdirs.sh

django/manage.py migrate

django/manage.py check

make -C django/static/css check
make -C django/static/css

django/manage.py collectstatic --noinput -i \*.less -i Makefile -i todo
(cd htdocs/static/css/ ; ls *.css | egrep -v 'all.css|tinymce.css' | xargs rm)

touch django/website/wsgi.py
