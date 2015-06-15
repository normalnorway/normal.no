import os
from uuid import uuid4
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File as DjangoFile
#from django.conf import settings
from apps.cms.models import File

class Command(BaseCommand):
    help = 'Add file to CMS file archive'

    def add_arguments (self, parser):
        parser.add_argument ('filename', type=str)
        parser.add_argument ('-n', '--name', type=str)
        parser.add_argument ('--uuid', action='store_true')
        # @todo add help strings

    def handle (self, *args, **options):
        filename = options['filename']
        name = options.get ('name', None)
        #if not name: name = os.path.basename (filename) # else might be uuid
        urlname = None
        if options['uuid']:
            urlname = uuid4().hex + os.path.splitext (filename)[1]
        with open (filename, 'rb') as fp:
            obj = File.objects.create (name=name, file=DjangoFile (fp, urlname))
        self.stdout.write ('%d: %s: %s' % (obj.pk, obj.name, obj.file.url))

#        with open (filename, 'rb') as fp:
#            obj = File()
#            if name: obj.name = name
#            obj.file.save (name, DjangoFile (fp)) # must close DjangoFile?
#        url = os.path.join (settings.MEDIA_URL, obj.file.url)
#        self.stdout.write ('Created File %d: %s' % (obj.pk, url))
