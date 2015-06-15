from django.core.urlresolvers import reverse
from django.db import models
from tinymce4.models import HtmlField

class File (models.Model):
    '''File uploaded to the server (file archive)'''
    file = models.FileField (upload_to='cms/file')  # max_length = 100
    name = models.CharField (max_length=50, unique=True, blank=True)
    size = models.IntegerField (editable=False) # default = -1
    mimetype = models.CharField (max_length=50, blank=True, editable=False)
    description = models.TextField (blank=True)
    # fields: upload_date? (can check the file), charset?
    # image fields: caption, copyright, copyright_url (attribution), comment?

    # Note: can't use self.file.{path,url} before save() is called
    def save (self, *args, **kwargs):
        #is_new = self.pk is None
        #print type(self.file.file)
        self.size = self.file.size
        self.mimetype = getattr (self.file.file, 'content_type', '')
        if not self.name:   # set name from filename
            # @todo limit length of name
            #self.name = self.file.file.name.split ('.', 1)[0]
            # self.file.name            url (q: what about self.file.url?)
            # self.file.file.name       path
            #filename = os.path.basename (self.file.file.name)
            filename = self.file.name.split ('/')[-1]
            filename = filename.replace('_', ' ') # undo django's transform
            self.name = filename.split ('.', 1)[0]
        super(File, self).save (*args, **kwargs)

    def __unicode__ (self):
        return self.name

    # delete file when object is deleted
#    def delete (self, *args, **kwargs):
#        self.file.delete (save=False)




class Page (models.Model):
    url = models.CharField (max_length=150, unique=True) # rename address?
    title = models.CharField (max_length=75)    # unique=True?
    content = HtmlField()
    #css = models.TextField (blank=True, help_text='Extra css styles')
    # published = models.BooleanField()
    # in_menu = models.BooleanField()   # menu_name: default to title
    # template = models.CharField (max_length=75)
    # extra_acl: to allow users to edit a subset of the pages
    # changed = models.DateTimeField()

    def __unicode__ (self):
        return self.title

    def save (self, *args, **kwargs):
        # @todo prepend / if missing
        if not self.url: # populate url from title
            from django.utils.text import slugify
            self.url = slugify (self.title)
        super(File, self).save (*args, **kwargs)

#    def get_absolute_url (self):
#        return reverse ('page-detail', args=[self.pk])
