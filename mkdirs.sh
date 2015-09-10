#!/bin/sh

# Create directories needed to run the site

# manage.py collectstatic creates htdocs/static

# Uploaded media
mkdir -p htdocs/media
for dir in cms tinymce; do
    path=htdocs/media/$dir
    test -e $path && continue
    mkdir $path
    chmod g+w $path
    chgrp www-data $path
done

# Apache logs
install -o root -g root -m 750 -d logs

# Django logs
install -g www-data -m 770 -d django/logs

# Never fail. Needed for travis-ci.org. (See .travis.yml)
true