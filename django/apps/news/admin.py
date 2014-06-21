from django.contrib import admin
from .models import Article
from .models import Story
import re


class LinkOnlyFilter (admin.SimpleListFilter):
    def lookups (self, request, model_admin):
        return (('1', 'Yes'), ('0', 'No'))
    def queryset (self, request, queryset):
        v = self.value()
        if v == None: return queryset
        return queryset.filter (body__isnull = bool(int(v)))
    title = 'Link only?'
    parameter_name = 'body'



class ArticleAdmin (admin.ModelAdmin):
    ordering = ('-date',)
    date_hierarchy = 'date'
    search_fields = ('title', 'summary', 'body')
    list_display = ('date', 'title', 'domain', 'has_body')
    list_display_links = ('title',)
    list_filter = ('date', LinkOnlyFilter)
    list_per_page = 50  # default is 100

    # testing add static text (without overriding the template)
#    fields = ('foobar', 'date', 'url', 'title', 'summary', 'body')
#    readonly_fields = ('foobar',)
#    def foobar (self, instance):
#        return 'Hello <b>bold</b> world'

    # http://stackoverflow.com/questions/4067712/django-admin-adding-pagination-links-in-list-of-objects-to-top

    '''
    def save_model(self, request, obj, form, change):
        # XXX does not work. will strip blanks, but not trigger 'field required'
        #obj.summary = obj.summary.strip()
        obj.body = obj.body.strip()
        obj.save()
    '''


    # Dynamic fields
    def has_body (self, obj):
        #return obj.body != None
        # XXX not consistent use of None vs ''
        return obj.body!='' and obj.body!=None
    has_body.boolean = True
    has_body.short_description = 'Has body'
    #has_body.admin_order_field = 'body'

    # @todo urlparse instead of regex
    _re_domain = re.compile (r'^(http://)?(www\.)?([^/]+)', re.I)
    def domain (self, obj):
        #domain = self._re_domain.match (obj.url).group(2)
        if not obj.url: return ''  # url can be NULL
	match = self._re_domain.match (obj.url)
	if not match: return ''
        domain = match.group(3)
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
admin.site.register (Story)
