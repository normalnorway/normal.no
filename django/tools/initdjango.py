import sys
import os

os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "website.settings")

# Find project root and add to python path
path = os.getcwd()
while True:
    if os.path.exists (os.path.join (path, 'manage.py')):
        break
    if path == '/':
        sys.exit ('error: manage.py not found!')
    path = os.path.dirname (path)   # walk upwards

if path != os.getcwd():
    sys.path.insert (0, path)   # q: safer to append instead?


# Might get AppRegistryNotReady exception if not doing this:
import django
django.setup()


# Note: logging does not work without django.setup()
#import logging
#logger = logging.getLogger()
#logger.warn ('no more piza')
