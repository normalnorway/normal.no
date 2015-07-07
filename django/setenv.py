import os
path = os.path.dirname (os.path.realpath (__file__))

print 'export PYTHONPATH=%s' % path
print 'export DJANGO_SETTINGS_MODULE=website.settings'
