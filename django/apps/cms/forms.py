from django import forms
from .models import Page

class PageForm (forms.ModelForm):   # PageCreate & PageEdit in admin
    url = forms.CharField (required=False, help_text='Leave empty to auto-create from the title.')

    # Do custom permission check
    def clean_url (self):
        url = self.cleaned_data['url']
        if not url or url.startswith ('/sider/'):
            return url
        if not self._user.has_perm ('cms.create_root_pages'):
            raise forms.ValidationError ('You are not allowed to create global urls. Please prefix with "/sider/" or leave empty.')
            #raise forms.ValidationError ('You are not allowed to create global urls. Please use "/sider%s" instead.' % url)
        return url

    # Note: Meta.model not needed since only used for the admin.
