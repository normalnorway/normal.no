from django.conf.urls import patterns, include, url

urlpatterns = patterns ('apps.news',
    url(r'^$',                      'views.list',   name='news-list'),
    url(r'^(?P<news_id>\d+)/$',     'views.detail', name='news-detail'),

    url(r'^arkiv/$',                            'views.archive', name='news-archive'),
    url(r'^arkiv/page/(?P<page>[0-9]+|last)/$', 'views.archive'),
      # @note when using '|', urlresolvers.reverse() does not work

    url(r'^arkiv/(?P<year>\d{4})/$',                    'views.archive_year'),
    url(r'^arkiv/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'views.archive_month'),
)
