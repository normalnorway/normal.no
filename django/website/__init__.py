# -*- encoding: utf-8 -*-

# XXX Hack to override default form error messages
# http://stackoverflow.com/a/20146377
from django.forms import Field
Field.default_error_messages = {
    'required': u'Dette feltet er påkrevd',
}

# A Django administrative site is represented by an instance of
# django.contrib.admin.sites.AdminSite; by default, an instance of this
# class is created as django.contrib.admin.site
