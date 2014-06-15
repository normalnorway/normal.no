# encoding: utf-8

#from django.http import HttpResponse
from django.shortcuts import render, redirect
from core.shortcuts import render_to, get_http_status
from apps.news.forms import NewsTips1, NewsTips2
from apps.news.models import Article


@render_to ('test.html')
def test (request):
    return dict (name='Torkel')


def news_tips (request, url):
    if request.method == 'POST':
        form = NewsTips2 (request.POST)
        if form.is_valid():
            # @todo model.full_clean?
            Article.objects.create (url=url, **form.cleaned_data)
            exit()
            # @todo message user
            return redirect ('index')
    else:
        form = NewsTips2()
    return render (request, 'news/tips.html', dict(form=form, url=url))
    '''
    return render (request, 'news/tips.html', {
        'form': form,
        'url':  url,
    })
    '''



# @todo limit per ip
# Note: Will redirect if url is accepted.
#@render_to ('news:index.html')
@render_to ('index.html')
def index (request):
    if not request.method == 'POST':
        return dict(form=NewsTips1())

    #form = NewsTips1 (request.POST)
    form = NewsTips1 (request.POST.copy())
    if not form.is_valid():
        return dict (form=form)

    url = form.cleaned_data['url'].strip()
    if Article.objects.filter(url=url).exists():
        message = u'Den lenken har vi allerede. Ellers takk :)' # @todo show link
        form.errors['__all__'] = form.error_class ([message])
        # @todo helper form_error (form, u'error message')
        form.data['url'] = ''
    else:
        code = get_http_status (url)
        if code != 200:     # @todo not 4xx and not 5xx
            msg = u'Død lenke (%d)' % (code,)
            form.errors['__all__'] = form.error_class ([msg])
        else: return redirect ('news-tips', url=url)

    return dict (form=form)
