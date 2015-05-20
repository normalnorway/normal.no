#!/bin/sh -e
#
# Setup / bootstrap the system to run normal.no
# Only run this the first time the code is checked out.
# Should work on Debian and Ubuntu; but only tested on Debian.
#
# See also: docs/install
#

# TODO:
# rename install?
# TLS certificates
# Create secret-key
# touch NODEBUG
# Howto install database
# Make sure running in correct directory


## Debian packages
apt-get install libapache2-mod-wsgi
apt-get install python-imaging  # @todo switch to Pillow: pip install Pillow



## Python packages
#pip install Django
pip install -r requirements.txt



## Misc setup
#git submodule init



## Permissions
# @todo check that this works

install -g www-data -m 770 -d htdocs/media

chgrp www-data logs/
chmod 770 logs/

chgrp www-data db/
chmod 770 db/
# @todo db/normal.db
chown root:www-data db/newmembers
chmod u=rw,g=w,o= db/newmembers        # write-only for the apache user



## Apache
a2enmod mod_wsgi
a2enmod mod_expires
ln -s /srv/www/normal.no/apache.conf /etc/apache2/sites-available/normal.no
a2ensite normal.no
/etc/init.d/apache2 reload


exec update.sh
