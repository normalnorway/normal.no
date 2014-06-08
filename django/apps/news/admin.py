from django.contrib import admin
from .models import Article
from .models import Story
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



# testing. better to use MyCharField & MyTextField ?
from django import forms
class ArticleAdminForm (forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
    def clean_title (self):
        return self.cleaned_data['title'].strip()


class ArticleAdmin (admin.ModelAdmin):
    ordering = ('-date',)
    date_hierarchy = 'date'
    search_fields = ('title', 'summary', 'body')
    list_display = ('datefmt', 'title', 'domain', 'has_body')
    list_display_links = ('title',)
    list_filter = ('date', LinkOnlyFilter)
    list_per_page = 50  # default is 100

    # testing overriding form
    form = ArticleAdminForm

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
    def datefmt (self, obj):
        return obj.date.strftime ('%F')
    datefmt.short_description = 'date'
    datefmt.admin_order_field = 'date'

    def has_body (self, obj):
        # XXX not consistent use of None vs ''
        #return obj.body != None
        if obj.body=='' or obj.body==None:
            return False
        return True
    has_body.boolean = True
    has_body.short_description = 'Body?'
    #has_body.admin_order_field = 'body'

    _re_domain = re.compile (r'^http://(www\.)?([^/]+)', re.I)
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



#class StoryAdmin (admin.ModelAdmin):

admin.site.register (Article, ArticleAdmin)
admin.site.register (Story)
#admin.site.register (Story, StoryAdmin)
