# XXX Hack to modify flatpage form
# https://djangosnippets.org/snippets/1035/
# http://stackoverflow.com/questions/1833287/change-field-in-django-flatpages-admin

# Note: This file is loaded from website/urls.py, since it have to come
#       after autodiscover, because we can't unregister FlatPage until
#       it's already been registered.

# @todo better?
# http://django-tinymce.googlecode.com/svn/tags/release-1.5/docs/.build/html/usage.html#using-the-widget

from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from tinymce4.widgets import TinyMCE


from django.db import models
class MyFlatPageAdmin (FlatPageAdmin):
    formfield_overrides = {
        models.TextField: { 'widget': TinyMCE },
        #models.TextField: { 'widget': TinyMCE (attrs={'cols': 20, 'rows': 20}) },
    }

# Note: To only override widget for some fields (not every TextField), use
# formfield_for_dbfield (self, db_field, **kwargs)
# @see http://django-tinymce.googlecode.com/svn/tags/release-1.5/docs/.build/html/usage.html#the-flatpages-link-list-view


admin.site.unregister (FlatPage)
admin.site.register (FlatPage, MyFlatPageAdmin)
