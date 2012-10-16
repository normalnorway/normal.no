"""
WSGI config for normal.no project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.
"""

import os
import sys

# Add site root to the Python search path
# sys.path.append ('/srv/www/new.normal.no/django')
sys.path.insert (0, os.path.join (os.path.dirname(__file__), ".."))

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "website.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
