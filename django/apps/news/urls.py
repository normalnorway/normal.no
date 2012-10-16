from django.conf.urls import patterns, include, url

urlpatterns = patterns ('apps.news',
    url(r'^$',                      'views.list',   name='news-list'),
    url(r'^(?P<news_id>\d+)/$',     'views.detail', name='news-detail'),

    url(r'^archive/$',                              'views.archive', name='news-archive'),
    url(r'^archive/page/(?P<page>[0-9]+|last)/$',   'views.archive'),

    url(r'^archive/(?P<year>\d{4})/$',                      'views.archive_year'),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$',   'views.archive_month'),
)
