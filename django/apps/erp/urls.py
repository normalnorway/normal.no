from django.conf.urls import url
from . import views

urlpatterns = [
    url (r'^$', views.index, name='erp-index'),
    url (r'^mypage$', views.mypage, name='erp-mypage'),
#    url (r'^$', views.FileCreate.as_view(), name='profile'),
]
