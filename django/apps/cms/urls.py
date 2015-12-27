from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from . import views

urlpatterns = [
    url (r'^file/select/$', views.FileSelect.as_view(), name='file-select'),

    # raise_exception=True => 403 Forbidden instead of redirect to /admin

    url (r'^page/(?P<pk>\d+)/update/$',
         permission_required ('cms.change_page', raise_exception=True)(
            views.PageUpdate.as_view()),
         name='page-update'),

    url (r'^content/(?P<pk>\d+)/update/$',
         permission_required ('cms.change_content', raise_exception=True)(
             views.ContentUpdate.as_view()),
         name='content-update'),

    url (r'^info/$',             views.InfoList.as_view(),   name='info-list'),
    url (r'^info/(?P<pk>\d+)/$', views.InfoDetail.as_view(), name='info-detail'),
]
