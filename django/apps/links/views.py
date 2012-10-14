from django.shortcuts import render
from .models import Category, Link

# @todo can use 'regroup' template tag instead!
def index (request):
    data = {}
    for link in Link.objects.all():
        cid = link.category_id
        if not data.has_key(cid):
            data[cid] = dict(name=str(link.category), data=[])
            #data[cid] = dict(name=link.category, data=[]) # sort fails
        data[cid]['data'].append (link)

    categories = data.values()
    categories.sort (lambda a,b: cmp(a['name'], b['name']))

    return render (request, 'nettguide.html', {'categories': categories })
