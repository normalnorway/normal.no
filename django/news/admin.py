from news.models import Article, ArticleLink
from django.contrib import admin

#admin.site.register (Article)
#admin.site.register (ArticleLink)


#class ArticleLinkInline (admin.StackedInline):
class ArticleLinkInline (admin.TabularInline):
    model = ArticleLink
    extra = 3

# @todo 25 items per page
class ArticleAdmin (admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['title', 'summary', 'body']
    date_hierarchy = 'pub_date'
#    list_display = ('pub_date', 'title')
    inlines = [ArticleLinkInline]

admin.site.register (Article, ArticleAdmin)
