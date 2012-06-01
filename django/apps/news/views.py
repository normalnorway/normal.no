from django.shortcuts import render_to_response, get_object_or_404
from apps.news.models import Article


def index (request):
    return render_to_response ('news/index.html', {
        'list': Article.objects.all().order_by('pub_date')[:5],
    })


def item (request, news_id):
    return render_to_response ('news/item.html', {
        'item': get_object_or_404 (Article, pk=news_id)
    });

