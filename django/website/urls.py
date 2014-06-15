from django.conf.urls import patterns, include, url
#from django.views.generic import TemplateView
from django.contrib import admin

#from core.views import IndexView
#from core.views import index
#import core

admin.autodiscover()

urlpatterns = patterns('',
    #(r'^$', TemplateView.as_view (template_name='index.html')),
    #(r'^$', IndexView.as_view()),
    url(r'^$', 'core.views.index', name='index'),

    url(r'^test$', 'core.views.test'),

    #url(r'^news-tips/$', 'core.views.news_tips'),
    url(r'^news-tips/(?P<url>.*)$', 'core.views.news_tips', name='news-tips'),

    # @todo add '$'?
    url(r'^nyheter/', include ('apps.news.urls'), name='news'),

    url(r'^nettguide/$', 'apps.links.views.index', name='links'),
    # RedirectView: nettguide.html -> links/

    url(r'^aktuelt/$', 'apps.news.views.story_list', name='news-story-list'),
    url(r'^aktuelt/(?P<story_id>\d+)/$', 'apps.news.views.story_detail', name='news-story-detail'),

    (r'^admin/', include (admin.site.urls)),
)

'''
# The real, dirty secret is that if you're also using
# django.contrib.admin, and
# django.template.loaders.app_directories.load_template_source is in your
# template loaders, you can get your templates free too!
urlpatterns += patterns('django.contrib.auth',
    (r'^accounts/login/$','views.login', {'template_name': 'admin/login.html'}),
        (r'^accounts/logout/$','views.logout'),
    )


    # Files
    url(r'^files/list$',    'apps.files.views.list', name='file-list'),
#    url(r'^files/upload$',  'apps.files.views.upload'),

    # Images
    url(r'^images/editor_upload$', 'apps.images.views.editor_upload'),

    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
'''

# Hack to serve MEDIA_ROOT in dev mode
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
