from django.conf.urls import url
from feed import NewsFeed as RssView
from .views import ArchiveView, YearView, MonthView, ArticleDetailView
from .views import NewArticleView

# TODO:
# * /arkiv/page -> /arkiv/side
# * drop arkiv-prefix? but then need prefix on detailed view, else name
#   conflict between year and pk
# * use GET parameter instead of extra url for pagination?

urlpatterns = (
    url (r'^(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='news-detail'),

    url (r'^arkiv/$', ArchiveView.as_view(), name='news-archive'),
    url (r'^arkiv/page/(?P<page>[0-9]+)/$', ArchiveView.as_view(), name='news-archive-page'), # pagination
    url (r'^arkiv/(?P<year>\d{4})/$', YearView.as_view(), name='news-archive-year'),
    url (r'^arkiv/(?P<year>\d{4})/(?P<month>\d{1,2})/$', MonthView.as_view(), name='news-archive-month'),

    url (r'^ny/$', NewArticleView.as_view(), name='news-new'),

    url (r'^rss/$', RssView(), name='rss'),
)
