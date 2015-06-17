from django import forms
from .models import File

# FileCreateForm, FileAddForm

# not in use
class FileCreateForm (forms.ModelForm):
    class Meta:
        model = File
        fields = 'file', 'name', 'description'
