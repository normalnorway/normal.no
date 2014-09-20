# NOT IN USE ANYMORE!

# https://docs.djangoproject.com/en/1.7/howto/custom-template-tags/#template-tag-thread-safety

from django import template
from django.core.urlresolvers import reverse
#from django.utils.text import slugify  # django 1.5
from apps.links.models import Category
from apps.news.models import Article

register = template.Library()


@register.inclusion_tag('menu-sub.html')
def menu_links ():
    data = Category.objects.values('name')
    base = reverse ('links') + '#'
    for e in data:
        e['href'] = base + template.defaultfilters.slugify (e['name'])
    return { 'data': data }


# cache helper
# @todo ttl=None => default value? see how cache.set is implemented
from django.core.cache import cache
def cached (key, ttl, func):
    #return func()
    data = cache.get (key)
    if not data:
        data = func()
        cache.set (key, data, ttl)
    return data


@register.inclusion_tag('menu-sub.html')
def news_links ():
#    ckey = 'menu-news-dates'
#    dates = cache.get (ckey)
#    if not dates:
#        dates = Article.objects.dates('date', 'year', order='DESC')
#        cache.set (ckey, dates, 3600) # @todo can cache until next year

    dates = cached ('menu-news-dates', 3600, lambda:
        Article.objects.dates('date', 'year', order='DESC'))

    data = []
    base = reverse ('news-archive')
    #for date in Article.objects.dates('date', 'year', order='DESC'):
    for date in dates:
        data.append (dict(name=date.year, href=base+str(date.year)+'/'))
    return { 'data': data }


#@register.tag
#def foo ():
