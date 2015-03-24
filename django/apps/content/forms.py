from django.forms import ModelForm
from tinymce4.widgets import TinyMCE
from django.contrib.flatpages.models import FlatPage


# @todo when migrating away from flatpages, then don't need this
class PageEditForm (ModelForm):
    class Meta:
        model = FlatPage
        fields = 'title', 'content'
        widgets = dict (content = TinyMCE)
