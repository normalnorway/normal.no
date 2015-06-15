from django import forms
from .models import File

# FileCreateForm, FileAddForm

class FileCreateForm (forms.ModelForm):
    class Meta:
        model = File
        fields = 'file', 'name', 'description'
