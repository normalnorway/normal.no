from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article


def list (request):
    #articles = Article.objects.all().order_by('-date')[:25]
    pagesize = 25
    paginator = Paginator (Article.objects.all().order_by('-date'), pagesize)
    try:
        articles = paginator.page (request.GET.get('page'))
    except:
        articles = paginator.page (1)

    # @todo helper?
    low = (articles.number-1) * pagesize + 1
    high = low + pagesize
    count = articles.paginator.count
    if high > count: high = count

    return render (request, 'news/list.html', {
        'list': articles, 'low': low, 'high': high,
    })


def detail (request, news_id):
    return render (request, 'news/detail.html', {
        'item': get_object_or_404 (Article, pk=news_id)
        # @todo same name as DetailView uses. (object?)
    })
