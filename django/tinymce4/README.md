# Django TinyMCE 4

Note: This have no relations to the django-tinymce software.

The application can enable TinyMCE for one form field using the widget
keyword argument of Field constructors or for all textareas on a page
using a view.

@todo or models.HTMLField


## Forms

The TinyMCE widget can be enabled by setting it as the widget for
a formfield.

    from tinymce4.widgets import TinyMCE

    class MyForm (forms.Form)   # or forms.ModelForm
    ...
    body = forms.CharField (widget = TinyMCE)
    ...


## Models

In all other regards, HTMLField behaves just like the standard Django
TextField field type.

    # Like TextField, but with a TinyMCE widget
    from tinymce4.models import HTMLField

    class MyModel (models.Model):
    ...
    body = HTMLField (...)
    ...
