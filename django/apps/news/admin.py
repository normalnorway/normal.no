from django.contrib import admin
from .models import Article

# @todo 25 items per page
class ArticleAdmin (admin.ModelAdmin):
#    list_display = ('date', 'title')
    list_display = ('title', 'date')
    list_filter = ['date']
    search_fields = ['title', 'summary', 'body']
    date_hierarchy = 'date'

admin.site.register (Article, ArticleAdmin)
