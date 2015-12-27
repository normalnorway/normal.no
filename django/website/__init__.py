# -*- encoding: utf-8 -*-

# Do some monkey patching.

# XXX Hack to override default form error messages
# http://stackoverflow.com/a/20146377
# Note: Will affect both admin and the public site
from django.forms import Field
Field.default_error_messages = {
    'required': u'Dette feltet er påkrevd',
}


# Add css class to all forms and modelforms.
from django.forms import Form
Form.error_css_class = 'validation-error'
Form.required_css_class = 'required'

from django.forms import ModelForm
ModelForm.error_css_class = 'validation-error'
ModelForm.required_css_class = 'required'


# A Django administrative site is represented by an instance of
# django.contrib.admin.sites.AdminSite; by default, an instance of this
# class is created as django.contrib.admin.site
