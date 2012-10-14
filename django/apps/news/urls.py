from django.conf.urls import patterns, include, url

urlpatterns = patterns ('apps.news',
    url(r'^$',                      'views.list',   name='news-list'),
    url(r'^(?P<news_id>\d+)/$',     'views.detail', name='news-detail'),
)
