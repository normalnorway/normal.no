# -*- encoding: utf-8 -*-

# XXX Hack to override default form error messages
# http://stackoverflow.com/a/20146377
from django.forms import Field
Field.default_error_messages = {
    'required': u'Dette feltet er påkrevd',
}
