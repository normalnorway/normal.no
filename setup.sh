#!/bin/sh -e
#
# Setup / bootstrap the system to run normal.no under Apache
# Should work on Debian and Ubuntu; but only tested on Debian.
#
# See also: docs/install
#

# TODO:
# rename install?
# tls certificates (update: now in git)
# create site.ini
# create mysql database
# add all required apache modules
# don't hardcode path


## Debian packages
apt-get install libapache2-mod-wsgi
apt-get install mysql-server


## Python packages
pip install -r requirements.txt


## Apache setup
a2enmod mod_wsgi
a2enmod mod_expires
ln -s /srv/www/normal.no/apache.conf /etc/apache2/sites-available/normal.no.conf
a2ensite normal.no
apachectl graceful


exec update.sh
