from django.conf.urls import patterns, url

urlpatterns = patterns ('tinymce4.views',
    url (r'^upload/$', 'upload', name='tinymce-upload'),
)
