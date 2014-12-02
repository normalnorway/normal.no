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
    sys.path.insert (0, path)


#from apps.news.models import Article
#print Article.objects.all()[:5]
