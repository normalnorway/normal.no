# Not in use
# https://docs.djangoproject.com/en/dev/ref/forms/fields/#filefield
from django import forms


class FileForm (forms.Form):
    file = forms.FileField (
        label = 'Select a file',
        help_text = 'max. 42 megabytes',
    )

