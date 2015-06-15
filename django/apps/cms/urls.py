from django.conf.urls import url

from . import views

urlpatterns = [
    url (r'^file/add/$', views.FileCreate.as_view(), name='file-add'),
    url (r'^file/select/$', views.FileSelect.as_view(), name='file-select'),

    url (r'^page/$', views.PageList.as_view(), name='page-list'),
    url (r'^page/(?P<pk>\d+)/$', views.PageDetail.as_view(), name='page-detail'),
    url (r'^page/(?P<pk>\d+)/update/$', views.PageUpdate.as_view(), name='page-update'),
]
