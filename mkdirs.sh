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

# @todo do this if already exists
# Might/will be needed when runing ./manage.py as a regular user and
# with empty django/logs/. Then all files will be owned by the user running
# manage.py, but they must be writable by www-data
# XXX not needed for dev-systems
#chgrp www-data django/logs/*.log
#chmod 660 django/logs/*.log

# So can run: collectstatic
#$ chown -R torkel.torkel htdocs/static/


true
