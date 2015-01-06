from django.conf.urls import patterns, url
from feed import NewsFeed

"""
TODO:
/arkiv/page -> /arkiv/side
drop arkiv-prefix? but then need prefix on detailed view, else name conflict between year and pk
"""

urlpatterns = patterns ('apps.news',    # apps.news.views?
    #url (r'^$',                      'views.list',  name='news-list'),
    url (r'^(?P<news_id>\d+)/$',    'views.detail', name='news-detail'),

    url (r'^arkiv/$',                                   'views.archive', name='news-archive'),
    url (r'^arkiv/page/(?P<page>[0-9]+|last)/$',        'views.archive'),   # pagination. @todo name='news-archive-page'),
      # @note when using '|', urlresolvers.reverse() does not work
      #       so better to drop /arkiv/page/last ?
    url (r'^arkiv/(?P<year>\d{4})/$',                   'views.archive_year',   name='news-archive-year'),
    url (r'^arkiv/(?P<year>\d{4})/(?P<month>\d{1,2})/$','views.archive_month',  name='news-archive-month'),

    url (r'^rss/$', NewsFeed(), name='rss'),

    url (r'^ny/$', 'views.add_new', name='news-add-new'),

    # @todo
    #import views
    #views.YearView.as_view()
    # then drop asignment in views.py
)
