from django.conf.urls import patterns, include, url

urlpatterns = patterns ('news.views',
    url(r'^$',                      'index'),
    url(r'^(?P<news_id>\d+)/$',     'item'),
)
