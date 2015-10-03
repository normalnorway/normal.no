#!/bin/sh -e

# @todo make sure all files in django/logs/*.log is writable by www-data
# $ chown www-data.www-data django/logs/*.log
# $ chmod g+w django/logs/error.log

# Run this on the production server to update the code

if [ -n "$(git status -s -uno --porcelain)" ]; then
    echo "Aborting! Working tree is not clean:"
    git status -s -uno --porcelain
    exit 1
fi

echo -n commit
git rev-parse live

git pull

sh mkdirs.sh

django/manage.py migrate

django/manage.py check

make -C django/static/css check
make -C django/static/css

django/manage.py collectstatic --noinput -i \*.less -i Makefile
# Update: Can't do this when using ManifestStaticFileStorage
#         will delete css/all.f5706c9f57c9.css
#(cd htdocs/static/css/ ; ls *.css | egrep -v 'all.css|tinymce.css' | xargs rm)

touch django/website/wsgi.py
