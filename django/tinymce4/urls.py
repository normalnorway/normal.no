from django.conf.urls import patterns, url

# TODO
# - prefix urls. (/core/<view> or /tinymce/<view>)
#   A: already prefixed, see include in website/urls.py
# - named urls: tinymce:upload, tinymce:link-list ?
#   Q: can drop tinymce- prefix and use app_label instead?

from apps.content.views import page_list_json as page_list_json_view

urlpatterns = patterns ('tinymce4.views',
    url (r'^upload/$', 'upload', name='tinymce-upload'),

    # Note: You must provide this view your self!
    # XXX view name is already prefixed with tinymce4.views
    #url (r'^page-list/$', 'apps.content.view.page_list_json', name='tinymce-link-list'),
    url (r'^page-list/$', page_list_json_view, name='tinymce-link-list'),
)
