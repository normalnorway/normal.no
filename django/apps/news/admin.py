from django.contrib import admin
from .models import Article


class LinkOnlyFilter (admin.SimpleListFilter):
    def lookups (self, request, model_admin):
        return (('1', 'Yes'), ('0', 'No'))
    def queryset (self, request, queryset):
        v = self.value()
        if v == None: return queryset
        return queryset.filter (body__isnull = bool(int(v)))
    title = 'Has body?'
    parameter_name = 'body'



class ArticleAdmin (admin.ModelAdmin):
    ordering = ('-date',)
    date_hierarchy = 'date'
    search_fields = ('title', 'summary', 'body')
    list_display = ('date', 'title', 'domain', 'has_body')
    list_display_links = ('title',)
    list_filter = ('date', LinkOnlyFilter)
    list_per_page = 50  # default is 100

    # http://stackoverflow.com/questions/4067712/django-admin-adding-pagination-links-in-list-of-objects-to-top

    def has_body (self, obj):
        #return obj.body != None
        return obj.body!='' and obj.body!=None  # @todo only use null or ''
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
