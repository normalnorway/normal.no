from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

import website.admin

urlpatterns = patterns ('',
    url(r'^$',              'core.views.index',             name='index'),
    url(r'^nyhetsbrev/$',   'core.views.newsletter',        name='newsletter'),
    url(r'^bli-medlem/$',   'apps.support.views.index',     name='enroll'),
    url(r'^medlem/$',       'apps.support.views.index'),    # alias
    url(r'^opprop/$',       'apps.support.views.petition',  name='petition'),
    url(r'^nettguide/$',    'apps.links.views.index',       name='links'),

    (r'^nyheter/',  include ('apps.news.urls')),
    #(r'^nyheter/',  include ('apps.news.urls', namespace='news')),
    (r'^admin/',    include (admin.site.urls)),

    (r'^tinymce/',  include ('tinymce4.urls')),
)


# Hack to serve MEDIA_ROOT in dev mode
# And to map a test view to /test
from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += patterns ('', url(r'^test/$', 'core.views.test'))
