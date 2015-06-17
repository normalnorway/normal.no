from django.conf.urls import patterns, url

# TODO
# - prefix urls. (/core/<view> or /tinymce/<view>)
#   A: already prefixed, see include in website/urls.py
# - named urls: tinymce:upload, tinymce:link-list ?
#   Q: can drop tinymce- prefix and use app_label instead?

from apps.cms.views import page_list_json

urlpatterns = patterns ('tinymce4.views',
    url (r'^upload/$', 'upload', name='tinymce-upload'), # q: is name in use?

    # Note: You must provide this view your self!
    url (r'^page-list/$', page_list_json),

    # don't work to import view by string
    #url (r'^page-list/$', 'apps.content.view.page_list_json', name='tinymce-link-list'),
)
