# encoding: utf-8
from django.http import HttpResponse
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import admin

from apps.content.views import PageEditView, BlockEditView

import website.admin

urlpatterns = [
    url(r'^$',              'core.views.index',             name='index'),
    url(r'^nyhetsbrev/$',   'core.views.newsletter',        name='newsletter'),
    url(r'^bli-medlem/$',   'apps.support.views.index',     name='enroll'),
    url(r'^opprop/$',       'apps.support.views.petition',  name='petition'),
    url(r'^nettguide/$',    'apps.links.views.index',       name='links'),

    url(r'^nyhetsbrev/1/$', TemplateView.as_view (template_name='newsletter-1.html')),

    # Redirect deprecated urls
    # @todo can redirect to named view instead
    url(u'^medlem/$', RedirectView.as_view (url='/bli-medlem/', permanent=True)),
    url(r'^rss/$', RedirectView.as_view (url='/nyheter/rss/', permanent=True)),
    url(u'^gruppes??ksmaal/$', RedirectView.as_view (url='/sider/gruppesoksmaal/', permanent=True)),
    url(u'^frivillig/$', RedirectView.as_view (url='/sider/frivillig/', permanent=True)),

    url(r'^nyheter/',  include ('apps.news.urls')),
    url(r'^tinymce/',  include ('tinymce4.urls')),

    # Non-admin forms
    url(r'^edit/page/(?P<pk>\d+)/$', login_required(PageEditView.as_view()), name='edit-page'),
    url(r'^edit/block/(?P<pk>\d+)/$', permission_required('flatpage.change_flatpage_gsf', raise_exception=True)(BlockEditView.as_view()), name='edit-block'),

    # https://docs.djangoproject.com/en/1.7/topics/auth/default/
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # need registration/login.html template

    # Password reset
    url(r'^admin/password_reset/$',                             auth_views.password_reset,          name='admin_password_reset'),
    url(r'^admin/password_reset/done/$',                        auth_views.password_reset_done,     name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',  auth_views.password_reset_confirm,  name='password_reset_confirm'),
    url(r'^reset/done/$',                                       auth_views.password_reset_complete, name='password_reset_complete'),

    # Google webmasters verification
    url(r'^google5b6561fca1bd3c25.html/$', lambda nil:
        HttpResponse ('google-site-verification: google5b6561fca1bd3c25.html')),

    # Note: Must be *after* passrod reset links!
    #(r'^admin/', lambda nil: HttpResponse ('<strong>Sorry, admin is temporarily closed due to maintenance!</strong>')),
    url(r'^admin/',    include (admin.site.urls)),
    url(r'^polls/', include('apps.polls.urls',  namespace="polls")),
]


# Hack to serve MEDIA_ROOT in dev mode
# And to map a test view to /test/
from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^test/$', 'core.testviews.test')]


# Hack to add custom permission to the FlatPage model
# A better fix is to inherit and add extra permissions to that model.
from django.contrib.auth.models import Permission
if not Permission.objects.filter (codename='change_flatpage_gsf').exists():
    from django.contrib.flatpages.models import FlatPage
    from django.contrib.contenttypes.models import ContentType
    ctype = ContentType.objects.get_for_model (FlatPage)
    Permission.objects.create (codename = 'change_flatpage_gsf',
                               name = 'Can change GSF-pages',
                               content_type = ctype)
