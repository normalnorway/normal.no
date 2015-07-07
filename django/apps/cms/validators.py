import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

#_slug_re = re.compile (r'^[-a-z0-9]+$')
#validate_url_path = RegexValidator (_slug_re, u'Enter a valid url path consisting of letters, numbers or hyphens.')

_slug_re = re.compile (r'^/(([-a-z0-9]+)/)+$')
validate_url_path = RegexValidator (_slug_re, u'Enter a valid url path consisting of letters, numbers or hyphens. It must begin and end with a slash.')


#def validate_startswith_slash (value):
#    if not value.startswith ('/'):
#        raise ValidationError ('Must begin with a slash. Example: /about/contact/')
