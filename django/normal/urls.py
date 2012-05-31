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

#    (r'^images/$', 'apps.images.views.index'),

    # @todo move to user app
    # Map default settings.LOGIN_URL to login view.
    # This requires this template: registration/login.html
#    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {
        'template_name': 'users/login.html',
    }),
    (r'^accounts/logout/$', 'apps.users.views.logout'),
    #(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    #  logout view shows admin logout template
    #  update: can redirect with: next_page
    #          or use: template_name='registration/logged_out.html'
    # @todo settings.LOGIN_REDIRECT_URL is used if no next URL parameter. It
    #       defaults defaults to /accounts/profile/

    url(r'^files/list$', 'apps.files.views.list', name='list'),
    # @note name is for shortname used in reverse (url template tag)
#    (r'^files/list$', 'apps.files.views.list'),
#    (r'^files/test$', 'apps.files.views.test', {'name':123, 'color':'red'}),

    #url(r'^files/test$', 'apps.files.views.test', {}, name='torkel'),
    # 'name' (url name) => used with reverse() or url template tag

#    (r'^news/', include ('news.urls')),

    (r'^admin/', include (admin.site.urls)),
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)


# Hack to serve MEDIA_ROOT in dev mode
if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
