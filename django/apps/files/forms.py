# https://docs.djangoproject.com/en/dev/ref/forms/fields/#filefield
from django import forms


# raise forms.ValidationError( msg )
# @see http://djangosnippets.org/snippets/103/


class FileForm (forms.Form):

    file = forms.FileField (
        label = 'Select a file',
        help_text = 'max. 42 megabytes',
    )
    #name = forms.CharField (label='Name', recuired=False)
    name = forms.CharField (
        label = 'Name',
        required = False,
        help_text = 'Defaults to filename'
    )

    # Testing
    def clean_file (self):
        file = self.cleaned_data['file']
#        print type(file)
        print file.content_type
        print file.charset
        print file.name
        print file.size     # _size also works
        #print file.temporary_file_path

        #raise forms.ValidationError(_('File type is not supported'))

        return file
