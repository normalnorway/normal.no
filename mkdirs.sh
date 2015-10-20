#!/bin/sh

# Create directories needed to run the site.
# Must also run 'manage.py collectstatic' to create htdocs/static

# todo: warn if permissions are wrong on django logs
# $ chown www-data.www-data django/logs/*.log
# $ chmod g+w django/logs/error.log


# Uploaded media
mkdir -p htdocs/media
for dir in cms tinymce cms/file cms/page; do
    path=htdocs/media/$dir
    #test -e $path && continue
    test -e $path || mkdir $path
    chmod g+w $path
    chgrp www-data $path
done

# Apache logs
install -o root -g root -m 750 -d logs

# Django logs. Group writable so regular user can run update.sh
install -g www-data -m 770 -d django/logs

# Never fail. Needed for travis-ci.org. (See .travis.yml)
true
