# If you don't want to use the built-in views, but want the convenience
# of not having to write forms for this functionality, the
# authentication system provides several built-in forms:
# https://docs.djangoproject.com/en/1.4/topics/auth/#built-in-forms

from django import forms
from django.contrib.auth.forms import UserCreationForm
#from apps.users.models import Profile


#class NewUserForm (forms.ModelForm):
#    class Meta:
#        model = Profile


class RegistrationForm (UserCreationForm):
    avatar = forms.ImageField (required = False,
                               help_text="Will be cropped to 100x100 pixels.")
    country = forms.CharField (required = False)

