import urlparse
from django.contrib import admin
from .models import Article


@admin.register (Article)
class ArticleAdmin (admin.ModelAdmin):
    ordering = ('-date',)
    date_hierarchy = 'date'
    fields = ('date', ('url', 'url_is_canonical'), 'title', 'summary', 'body', 'image_url', 'published', 'user')
    search_fields = ('title', 'summary', 'body', 'url')
    actions = ('action_publish',)
    list_display = ('_date', 'title', '_domain', 'published', 'has_summary', 'has_body')
    list_display_links = ('_date', 'title',)
    list_filter = ('date', 'published')
    list_per_page = 50  # default is 100

    def action_publish (self, request, queryset):
        queryset.update (published=True)
    action_publish.short_description = 'Publiser valgte nyhets-lenker'

    def _date (self, obj):
        if obj.date: return obj.date.strftime ('%F')
        #return obj.date.strftime ('%F')
        # Q: for which objects are date missing? A: auto-added, with unparsable data
    _date.admin_order_field = 'date'
    _date.short_description = 'date'

    def _domain (self, obj):
        urlobj = urlparse.urlsplit (obj.url)
        s = urlobj.hostname
        domain = s[4:] if s.startswith('www.') else s # bug: messes up sorting
        return '<a href="%s" title="%s" target="_blank">%s</a>' % (obj.url, obj.url, domain)
    _domain.allow_tags = True
    _domain.short_description = 'Domene'
    _domain.admin_order_field = 'url'

    def has_body (self, obj):
        return obj.body != ''
    has_body.boolean = True
    has_body.short_description = 'own comment'
    has_body.admin_order_field = 'body'

    def has_summary (self, obj):
        return bool(obj.summary)
    has_summary.boolean = True
    has_summary.admin_order_field = 'summary'
