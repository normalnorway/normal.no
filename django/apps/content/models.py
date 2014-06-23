from django.db import models


# @todo mark returned string as safe?
def get_content (name):
    ''' Return content block by name. If not found, substitute empty string'''
    try:
        obj = Content.objects.get (name=name)
    except Content.DoesNotExist:
        return ''   # @todo log
    return obj.content


# @todo fetch all args with one sql-query
def get_content_dict (*args):
    '''Return dict with name,content'''
    ctx = dict()
    for arg in args:
        key = arg.replace ('-', '_')  # django template vars can't contain '-'
        ctx[key] = get_content (arg)
    return ctx



class Content (models.Model):
    ''' Content block used by various views/templates '''
    name = models.CharField (max_length=64, unique=True)
    content = models.TextField (blank=True)
    def __unicode__ (self): return self.name
