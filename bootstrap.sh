#!/bin/sh -e

pip install -r requirements.txt

# @todo bootstrap db
#if [ ! -e db/normal.db ]; then

mkdir -p logs

chgrp www-data django/logs
chmod g+w django/logs

chown root:www-data db/newmembers
chmod u=rw,g=w,o=   db/newmembers   # write-only for the apache user
