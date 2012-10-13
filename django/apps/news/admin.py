from django.contrib import admin
from .models import Article
import re

class LinkOnlyFilter (admin.SimpleListFilter):
    title = 'Link only?'
    parameter_name = 'body'
    def lookups(self, request, model_admin):
        return (('1', 'Yes'), ('0', 'No'))
    def queryset(self, request, queryset):
        v = self.value()
        if v == None: return queryset
        return queryset.filter (body__isnull = bool(int(v)))


class ArticleAdmin (admin.ModelAdmin):
    list_display = ('datefmt', 'title', 'domain', 'has_body')
    list_display_links = ('title',)
    ordering = ('-date',)
    list_per_page = 50  # default is 100
    list_filter = ('date', LinkOnlyFilter)
    search_fields = ('title', 'summary', 'body')
    date_hierarchy = 'date'

    # http://stackoverflow.com/questions/4067712/django-admin-adding-pagination-links-in-list-of-objects-to-top

    _re_domain = re.compile (r'^http://(www\.)?([^/]+)', re.I)

    # Dynamic fields
    def datefmt (self, obj):
        return obj.date.strftime ('%F')
    datefmt.short_description = 'date'
    datefmt.admin_order_field = 'date'

    def has_body (self, obj):
        return obj.body != None
    has_body.boolean = True
    has_body.short_description = 'Body?'
    #has_body.admin_order_field = 'body'

    def domain (self, obj):
        #return self._re_domain.match (obj.url).group(2)
        domain = self._re_domain.match (obj.url).group(2)
        return '<a href="%s" title="%s" target="_blank">%s</a>' % (obj.url, obj.url, domain)
    domain.allow_tags = True
    domain.short_description = 'URL'
    domain.admin_order_field = 'url'

    '''
    def get_actions (self, request):
        actions = super(ArticleAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['delete_selected']
        return actions
    '''


admin.site.register (Article, ArticleAdmin)
