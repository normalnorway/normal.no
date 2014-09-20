# Context processors gives the ability to pass any variable to templates.

# https://docs.djangoproject.com/en/1.7/_modules/django/core/context_processors/

# In your settings.py add 'core.context.my_context' to
# TEMPLATE_CONTEXT_PROCESSORS in settings.py.

# NOT IN USE

def my_context (request):
    """Put MyUser object of logged-in user into 'my_user' template var"""
    try:
        return dict (my_user = MyUser.objects.get(user=request.user))
    except ObjectNotFound:
        return dict (my_user = '')
        #return { 'my_user': None }
