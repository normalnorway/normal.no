# Hack. Will run before app is fully initialized, I think ...
#from django.template.base import add_to_builtins
#add_to_builtins ('apps.cms.templatetags.cms')

# Update:
# Projects should now define built-in libraries via the 'builtins' key of
# OPTIONS when defining a DjangoTemplates backend.
