import urlparse
from django.contrib import admin
from .models import Article


# @todo can drop this. can achieve the same by sorting by has_body
class LinkOnlyFilter (admin.SimpleListFilter):
    def lookups (self, request, model_admin):
        return (('1', 'Yes'), ('0', 'No'))
    def queryset (self, request, queryset):
        v = self.value()
        if v is None: return queryset
        if v == '0': return queryset.filter (body='')
        if v == '1': return queryset.exclude (body='')
        assert False
    title = 'Own comment'
    parameter_name = 'body'



class ArticleAdmin (admin.ModelAdmin):
    ordering = ('-date',)
    date_hierarchy = 'date'
    fields = ('date', ('url', 'url_is_canonical'), 'title', 'summary', 'body', 'image_url', 'published')
    search_fields = ('title', 'summary', 'body')
    actions = ('action_publish',)
    list_display = ('_date', 'title', '_domain', 'published', 'has_body')
    list_display_links = ('_date', 'title',)
    list_filter = ('date', 'published', LinkOnlyFilter)
    list_per_page = 50  # default is 100

    def action_publish (self, request, queryset):
        queryset.update (published=True)
    action_publish.short_description = 'Publiser valgte nyhets-lenker'

    def _date (self, obj):
        if obj.date: return obj.date.strftime ('%F')
        #return obj.date.strftime ('%F') # Q: for which objects are date missing?
    _date.admin_order_field = 'date'
    _date.short_description = 'date'

    # http://stackoverflow.com/questions/4067712/django-admin-adding-pagination-links-in-list-of-objects-to-top

    def has_body (self, obj):
        return obj.body != ''
    has_body.boolean = True
    has_body.short_description = 'own comment'
    has_body.admin_order_field = 'body'

    def _domain (self, obj):
        urlobj = urlparse.urlsplit (obj.url)
        s = urlobj.hostname
        domain = s[4:] if s.startswith('www.') else s
        return '<a href="%s" title="%s" target="_blank">%s</a>' % (obj.url, obj.url, domain)
    _domain.allow_tags = True
    _domain.short_description = 'Domene'
    _domain.admin_order_field = 'url'


admin.site.register (Article, ArticleAdmin)
