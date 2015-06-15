import os
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File as DjangoFile
from apps.cms.models import File

# TODO
# - remove stale files. or just pipe to xargs rm
# - rm: handle more than one arg
# /home/torkel/dev/python/examples/argparse2.py

class Command(BaseCommand):
    help = 'Manage files'

    def add_arguments (self, parser):
        parser.add_argument ('myargs', nargs='*', type=str, default=['show'])
        # @todo auto-fill choices from do_* members. use docstring as help text
        #parser.add_argument ('command', nargs=2, type=str)
        #parser.add_argument ('command', nargs='?', type=str, default='foo')
        #parser.add_argument ('command', type=str, choices=['ls', 'show', 'stale', 'missing', 'rmall'])
        #parser.add_argument ('command', type=str, default='show') don't work
        #parser.add_argument('--ids', nargs='+', type=int)

    def handle (self, *args, **options):
        args = options['myargs']
        cmd = args.pop (0)
        handler = getattr (self, 'do_'+cmd, None)
        if handler:
            handler (*args)
        else:
            raise CommandError ('No such command: %s' % cmd)

    def do_ls (self):
        for obj in File.objects.all():
            self.stdout.write (obj.file.path)

    def do_show (self):
        for obj in File.objects.all():
            self.stdout.write ('%4d: %s' % (obj.pk, obj.name))

    def do_stale (self):
        # need to know path prefix, even if no objects in db
        prefix = '/home/torkel/www/htdocs/media/cms/file/'
        files = set (os.listdir (prefix))
        for obj in File.objects.all():
            name = os.path.basename (obj.file.path)
            if name in files: files.remove (name)
        for name in files: self.stdout.write (name)

    def do_missing (self):
        prefix = '/home/torkel/www/htdocs/media/cms/file/'
        files = set (os.listdir (prefix))
        for obj in File.objects.all():
            name = os.path.basename (obj.file.path)
            if name not in files:
                self.stdout.write ('%d:%s' % (obj.pk, obj.file.path))

    def do_rm (self, pk):
        obj = File.objects.get (pk=pk)
        dfile = obj.file
        obj.delete()
        dfile.delete (save=False)

    def do_rmall (self):
        for obj in File.objects.all():
            self.do_rm (obj.pk)


'''
    def do_add (self, filename):
        fp = open (filename, 'rb')
        name = os.path.basename (filename)
        name = name.translate (' ', '_') # @todo do same as django does
        #fileobj = DjangoFile (fp, name)
        fileobj = DjangoFile (fp)
        obj = File()
        obj.file.save (name, fileobj, save=False)
        obj.full_clean()
        obj.save()
        # @todo close fp & fileobj
'''
