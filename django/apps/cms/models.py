from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from tinymce4.models import HtmlField
from .validators import validate_url_path


class Content (models.Model):
    '''Content block used by various views/templates'''
    name = models.CharField (max_length=64, unique=True)
    content = HtmlField (blank=True)
    # changed = models.DateTimeField (auto_add_now=True)

    def __unicode__ (self): return self.name

#    class Meta:
#        verbose_name_plural = 'content'



class File (models.Model):
    '''File uploaded to the server (file archive)'''
    file = models.FileField (upload_to='cms/file')  # max_length = 100
    name = models.CharField (max_length=50, unique=True, blank=True)
    size = models.IntegerField (editable=False) # default = -1
    mimetype = models.CharField (max_length=50, blank=True, editable=False)
    description = models.TextField (blank=True)

    # Note: self.file.{path,url} might be changed by super().save(),
    # to make them unique (prefix is added).
    def save (self, *args, **kwargs):
        if self.size is None:
            self.size = self.file.size
        if not self.mimetype:
            self.mimetype = getattr (self.file.file, 'content_type', '')
        if not self.name:
            self.file.save (self.file.name, self.file.file, save=False)
            self.name = self.name_from_filename()
        super(File, self).save (*args, **kwargs)

    def name_from_filename (self):
        name = self.file.name           # url path
        name = name.split ('/')[-1]     # split filename from path
        name = name.split ('.', 1)[0]   # remove extension
        name = name.replace('_', ' ')   # undo django's transform
        name = name[0:self.file.field.max_length]   # limit length
        return name

    def __unicode__ (self):
        return self.name

    # Note: the delete() method for an object is not necessarily
    # called when deleting objects in bulk using a QuerySet.
    # So better to use a signal. Or just keep the files around.
#    def delete (self, *args, **kwargs):
#        self.file.delete (save=False)



class Page (models.Model):
    title = models.CharField (max_length=75, unique=True)
    url = models.CharField (max_length=83, unique=True, validators=[validate_url_path])
    content = HtmlField()
    modified = models.DateTimeField (auto_now=True)
    published = models.BooleanField (default=True, help_text='When unchekced the page is not globally accessible.')
    summary = models.TextField (blank=True, help_text='Short summary used when sharing the page on social media.')
    image = models.FileField (blank=True, upload_to='cms/page', help_text='Image used when sharing the page on social media. When unset, Normals logo is used.')

    def save (self, *args, **kwargs):
        if not self.url: # populate url from title
            self.url = '/sider/' + slugify (self.title)
        if not self.url.endswith('/'): self.url += '/'
        super(Page, self).save (*args, **kwargs)

    def get_absolute_url (self):
        return self.url

    def __unicode__ (self):
        return self.title

    class Meta:
        permissions = (
            ('create_root_pages', 'Can create non-restricted page urls'),
        )
