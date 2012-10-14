from django.shortcuts import render, render_to_response, get_object_or_404
from apps.news.models import Article


def list (request):
    articles = Article.objects.all().order_by('-date')[:25]
    return render (request, 'news/list.html', { 'list': articles })


def detail (request, news_id):
    item = get_object_or_404 (Article, pk=news_id)
    return render (request, 'news/detail.html', { 'item': item })
