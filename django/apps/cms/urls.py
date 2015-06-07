from django.conf.urls import url

# Prefix with 'cms'; then use these conventions:
# /cms/page/<id>
# /cms/page/edit/<id>
# /cms/block/<id>
# /cms/block/edit/<id>

from apps.cms import views
#import .views as views ?

urlpatterns = [
    url (r'^(?P<pk>\d+)/$', views.PageDetail.as_view(), name='page-detail'),
]
