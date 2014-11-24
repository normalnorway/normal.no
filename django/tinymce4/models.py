from django.db import models
from .widgets import TinyMCE


class HtmlField (models.TextField):
    description = 'Like TextField, but with a TinyMCE widget'

    def formfield (self, **defaults):
        defaults['widget'] = TinyMCE
        return super(HtmlField,self).formfield (**defaults)
