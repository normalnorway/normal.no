from django.conf.urls import url

from . import views

#from django.contrib.auth.decorators import login_required, permission_required
# login_required(PageEditView.as_view())
# permission_required ('flatpage.change_flatpage_gsf', raise_exception=True)(BlockEditView.as_view())

urlpatterns = [
    url (r'^file/add/$', views.FileCreate.as_view(), name='file-add'),
    url (r'^file/select/$', views.FileSelect.as_view(), name='file-select'),

    #url (r'^page/$', views.PageList.as_view(), name='page-list'),
    #url (r'^page/(?P<pk>\d+)/$', views.PageDetail.as_view(), name='page-detail'),
    url (r'^page/(?P<pk>\d+)/update/$', views.PageUpdate.as_view(), name='page-update'),

    url (r'^content/(?P<pk>\d+)/update/$', views.ContentUpdate.as_view(), name='content-update'),
]

# NAMING CONVENTION
#
# URL                   View Class      URL Name
# ------------------------------------------------
# /page/                PageList        page-list
# /page/<pk>/           PageDetail      page-detail
# /page/<pk>/update/    PageUpdate      page-update
#
#
# BETTER?
#
# URL                   View Class      URL Name
# ------------------------------------------------
# /page                 PageList        page-list
# /page/<pk>/           PageItem        page-item   (or just page?)
# /page/<pk>/edit       PageEdit        page-edit
