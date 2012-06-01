from django.conf.urls import patterns, include, url

# Alternative approach:
# from . import views
#   r'(... , views.index),
#   r'(... , views.item),


urlpatterns = patterns ('apps.news.views',
    url(r'^$',                      'index'),
    url(r'^(?P<news_id>\d+)/$',     'item'),
)
