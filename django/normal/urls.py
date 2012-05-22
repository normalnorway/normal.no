from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()
# import has to come after autodiscover, because we can't 
# unregister FlatPage until it's already been registered.
#import site.admin


urlpatterns = patterns('',
    (r'^$', TemplateView.as_view (template_name='index.html')),
#    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/home/'}),

    (r'^images/$', 'apps.images.views.index'),

    (r'^files/list$', 'apps.files.views.list'),
#    (r'^files/foo$', 'listview', name='apps.files.foo'),
#    (r'^files/list$', 'listview', name='apps.files.list'),

#    (r'^news/', include ('news.urls')),

    (r'^admin/', include (admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)


# Hack to serve MEDIA_ROOT in dev mode
# https://docs.djangoproject.com/en/1.4/howto/static-files/#serving-other-directories
# https://docs.djangoproject.com/en/1.4/ref/contrib/staticfiles/#static-file-development-view
# '/static' is automatically enabled by runserver (when DEBUG is True)
# + static ('/my/url', document_root='/my/path')

if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
