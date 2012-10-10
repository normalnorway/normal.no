'''
Init Django. So it can be used from command line scripts, etc.

NOTE: Assumes project root is parent path.
TODO: fix. howto pass? (walk path upwards until find manage.py?)
'''

import sys
import os


# Set if not already set
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "website.settings")
#os.environ["DJANGO_SETTINGS_MODULE"] = 'website.settings'

# Add project root to path (i.e., parent directory)
sys.path.insert (0, os.path.join (
    os.path.dirname (os.path.abspath(__file__)),
    os.pardir))


#import django
from django.core.management import setup_environ
from website import settings

setup_environ (settings)


# Add parent path (project root) to PYTHONPATH
#s = os.path.abspath (__file__)
#s = os.path.dirname (s)
#s = os.path.normpath (os.path.join(s, os.pardir))
#sys.path.append (s)
