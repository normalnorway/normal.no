from django.db import models
#from tinymce4.widgets import TinyMCE
from .widgets import TinyMCE


class HTMLField (models.TextField):
    description = 'Like TextField, but with a TinyMCE widget'

    def formfield (self, **defaults):
        defaults['widget'] = TinyMCE
        return super(HTMLField,self).formfield (**defaults)
