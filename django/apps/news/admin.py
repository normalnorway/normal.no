from django.contrib import admin
from .models import Article


class LinkOnlyFilter (admin.SimpleListFilter):
    def lookups (self, request, model_admin):
        return (('1', 'Yes'), ('0', 'No'))
    def queryset (self, request, queryset):
        v = self.value()
        if v == None: return queryset
        if v == '0': return queryset.filter (body='')
        if v == '1': return queryset.exclude (body='')
        assert False
    title = 'Has body?'
    parameter_name = 'body'



class ArticleAdmin (admin.ModelAdmin):
    ordering = ('-date',)
    date_hierarchy = 'date'
    fields = ('date', ('url', 'url_is_canonical'), 'title', 'summary', 'body', 'image_url', 'published')
    search_fields = ('title', 'summary', 'body')
    list_display = ('_date', 'title', 'domain', 'published', 'has_body')
    list_display_links = ('_date', 'title',)
    list_filter = ('date', 'published', LinkOnlyFilter)
    list_per_page = 50  # default is 100

    def _date (self, obj):
        if obj.date: return obj.date.strftime ('%F')
        # Q: for which objects are date missing?
        #return obj.date.strftime ('%F')
    _date.admin_order_field = 'date'
    _date.short_description = 'date'

    # http://stackoverflow.com/questions/4067712/django-admin-adding-pagination-links-in-list-of-objects-to-top

    def has_body (self, obj):
        return obj.body != ''
    has_body.boolean = True
    has_body.short_description = 'Has body'
    #has_body.admin_order_field = 'body'

    # @todo urlparse instead of regex
    import re
    _re_domain = re.compile (r'^(http://)?(www\.)?([^/]+)', re.I)
    def domain (self, obj):
        #domain = self._re_domain.match (obj.url).group(2)
        if not obj.url: return ''  # url can be NULL
        match = self._re_domain.match (obj.url)
        if not match: return ''
        domain = match.group(3)
        return '<a href="%s" title="%s" target="_blank">%s</a>' % (obj.url, obj.url, domain)
    domain.allow_tags = True
    domain.short_description = 'Lenke'
    domain.admin_order_field = 'url'



admin.site.register (Article, ArticleAdmin)
