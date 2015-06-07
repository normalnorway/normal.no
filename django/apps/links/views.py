from django.shortcuts import render
from .models import Link

# @todo can use 'regroup' template tag instead!
# @todo optimize into one sql query
def index (request):
    data = {}
    for link in Link.objects.all():
        cid = link.category_id
        if not cid in data:
            data[cid] = dict(name=str(link.category), data=[])
            #data[cid] = dict(name=link.category, data=[]) # sort fails
        data[cid]['data'].append (link)

    categories = data.values()  # list of used categories
    categories.sort (lambda a,b: cmp(a['name'], b['name']))

    return render (request, 'nettguide.html', {'categories': categories })
