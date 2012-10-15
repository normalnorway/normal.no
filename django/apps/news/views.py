from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article
from .forms import SearchForm
#import forms   # forms.Search


def list (request):
    # Search
    query = request.GET.get ('query')
    if query:
        form = SearchForm (request.GET)
        qs = Article.objects.filter(
                Q(title__icontains=query)   |
                Q(summary__icontains=query) |
                Q(body__icontains=query)
        )
    else:
        form = SearchForm()
        qs = Article.objects.all()

    qs = qs.order_by('-date')

    # Pagination
    pagesize = 25
    paginator = Paginator (qs, pagesize)
    try:
        articles = paginator.page (request.GET.get('page'))
    except:
        articles = paginator.page (1)
    # @todo helper?
    # @todo hi+low, and put on paginator instance
    low = (articles.number-1) * pagesize + 1
    high = low + pagesize
    count = paginator.count
    if high > count: high = count

    return render (request, 'news/list.html', {
        'list': articles, 'low': low, 'high': high,
        'form': form, 'query': query,
        # if query: search = '&search=%s' % urlencode(query)
        # better to pass in session?
    })



def detail (request, news_id):
    return render (request, 'news/detail.html', {
        'item': get_object_or_404 (Article, pk=news_id)
        # @todo same name as DetailView uses. (object?)
    })
