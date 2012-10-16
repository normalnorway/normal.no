from django import template
from django.core.urlresolvers import reverse
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


@register.inclusion_tag('menu-sub.html')
def news_links ():
    data = []
    base = reverse ('news-archive')
    for date in Article.objects.dates('date', 'year', order='DESC'):
        data.append (dict(name=date.year, href=base+str(date.year)+'/'))
    return { 'data': data }


#@register.tag
#def foo ():
