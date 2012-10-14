from django.contrib import admin
from django.forms.models import fields_for_model
from .models import Guide, Category
import re

class GuideAdmin (admin.ModelAdmin):
    #ordering = ('category',)
    #ordering = ('category__name',)
    list_display = ('name', 'category', 'url_')

    # Dynamically construct fieldset
    def __init__ (self, *args, **kwargs):
        super(GuideAdmin,self).__init__ (*args, **kwargs)
        fields = fields_for_model (self.model).keys()
        fields.remove ('comment')
        fields.remove ('lang')
        self.fieldsets = (
            (None, { 'fields': (fields) }),
            ('Extra', {
                'fields':   ('lang', 'comment'),
                #'fields':   ('comment',),
                'classes':  ('collapse',),
            }),
        )
    # @todo convert into decorator?
    # http://stackoverflow.com/questions/2420516/how-to-collapse-just-one-field-in-django-admin
    # @fieldsets_collapse (['comment'], label='Internal')

    def url_ (self, obj):
        m = self.url_.regex.match (obj.url)
        s = m.group(1)
        if m.end() == len(obj.url):
            return '<a href="%s" target="_blank">%s</a>' % (obj.url, s)
        else:
            return '<a href="%s" target="_blank" title="%s">%s &hellip;</a>' % (obj.url, obj.url, s)
    url_.allow_tags = True
    url_.short_description = 'URL'
    url_.admin_order_field = 'url'
    url_.regex = re.compile (r'^http://([^/]+)(/?)', re.I)


admin.site.register (Guide, GuideAdmin)
admin.site.register (Category)
