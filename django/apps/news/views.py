from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article
from .forms import SearchForm
#import forms   # forms.Search

#from django.views.generic.dates
from django.views.generic import dates


class ArchiveView (dates.ArchiveIndexView):
    model = Article
    date_field = 'date'
    paginate_by = 25
    #context_object_name = 'list'    # object_list
    #date_list_period = 'year'
    #allow_future = False
    # get_dated_queryset(**lookup)
    # get_date_list(queryset, date_type=None, ordering='ASC')
archive = ArchiveView.as_view()

# ArchiveYearView
# @todo show months in revered order?
class YearView (dates.YearArchiveView):
    model = Article
    date_field = 'date'
    make_object_list = True     # False => only generate month list
archive_year = YearView.as_view()

# ArchiveMonthView
class MonthView (dates.MonthArchiveView):
    model = Article
    date_field = 'date'
    month_format = '%m'
    make_object_list = True
archive_month = MonthView.as_view()



# @note can use ArchiveIndexView as base for this view
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
