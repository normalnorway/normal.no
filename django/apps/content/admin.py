from django.db import models
from django.contrib import admin
from models import Content
from tinymce4.widgets import TinyMCE

# @todo use HtmlField in model instead

class ContentAdmin (admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: { 'widget': TinyMCE },
    }

admin.site.register (Content, ContentAdmin)
