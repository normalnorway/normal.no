from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.index', name='index'),

    url(r'^test/$', 'core.views.test'),

    url(r'^bli-medlem/$', 'apps.support.views.index'),   # enroll
    url(r'^news-tips/(?P<url>.*)$', 'core.views.news_tips', name='news-tips'),

    # Sections
    url(r'^nettguide/$', 'apps.links.views.index', name='links'),
    url(r'^aktuelt/$', 'apps.news.views.story_list', name='news-story-list'),
    url(r'^aktuelt/(?P<story_id>\d+)/$', 'apps.news.views.story_detail', name='news-story-detail'),

    url (r'^nyheter/', include ('apps.news.urls'), name='news'), # add '$'?

    (r'^admin/', include (admin.site.urls)),
)
'''
url (r'^nettguide/$',
     'apps.links.views.index',
     name='links'),

url (r'^aktuelt/$',
     'apps.news.views.story_list',
     name='news-story-list'),

url (r'^aktuelt/(?P<story_id>\d+)/$',
     'apps.news.views.story_detail',
     name='news-story-detail'),
'''



# Hack to serve MEDIA_ROOT in dev mode
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
