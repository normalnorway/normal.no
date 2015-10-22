import urlparse
from django.contrib import admin
from .models import Link, Category


@admin.register (Link)
class LinkAdmin (admin.ModelAdmin):
    list_display = ('name', 'category', 'lang', 'url_')
    list_filter = ('category', 'lang')
    ordering = ('category__name', 'name',)
    search_fields = ('name', 'url')

    # @fieldsets_collapse (['comment'], label='Internal')
    # http://stackoverflow.com/questions/2420516/how-to-collapse-just-one-field-in-django-admin

    def url_ (self, obj):
        o = urlparse.urlsplit (obj.url)
        if o.path=='/' and not o.query:
            return '<a href="%s">%s</a>' % (obj.url, o.hostname)
        return '<a href="%s" title="%s">%s &hellip;</a>' % (obj.url, obj.url, o.hostname)
    url_.allow_tags = True
    url_.short_description = 'URL'
    url_.admin_order_field = 'url'


@admin.register (Category)
class CategoryAdmin (admin.ModelAdmin):
    list_display = 'name',
