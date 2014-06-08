# encoding: utf-8

#from django.http import HttpResponse
from django.shortcuts import render, redirect

from apps.news.forms import NewsTips1, NewsTips2
from apps.news.models import Article

# @todo move to own file
# @todo what about fragments? normal.no/#doner
# http://docs.python-requests.org/en/latest/
import httplib
import urlparse
def get_http_status (urlstr):
    url = urlparse.urlsplit (urlstr)
    assert not url.query    # q: what to do with query string?
    try:
        conn = httplib.HTTPConnection (url.hostname)
        conn.request ('HEAD', url.path)
        return conn.getresponse().status
    except StandardError:
        return None



def news_tips (request, url):
    if request.method == 'POST':
        form = NewsTips2 (request.POST)
        if form.is_valid():
            Article.objects.create (url=url, **form.cleaned_data)
            exit()
            # @todo message user
            return redirect ('index')
    else:
        form = NewsTips2()

    return render (request, 'news/tips.html', {
        'form': form,
        'url':  url,
    })



def index (request):
    message = None
    if request.method == 'POST':
        #form = NewsTips1 (request.POST)
        form = NewsTips1 (request.POST.copy())
        if form.is_valid():
            url = form.cleaned_data['url'].strip()
            if Article.objects.filter(url=url).exists():
                message = u'Den lenken har vi allerede. Ellers takk :)'
                form.errors['__all__'] = form.error_class ([message])
                form.data['url'] = ''
                # @todo goto end / break out
                # @todo show link
                #message = 'Den lenken har vi allerede. Ellers takk :)'
                #form = NewsTips1()  # clear form (since bound)

            code = get_http_status (url)
            if code != 200: # @todo not 4xx and not 5xx
                msg = u'Død lenke (%d)' % (code,)
                form.errors['__all__'] = form.error_class ([msg])
            else:
                return redirect ('news-tips', url=url)
    else:
        form = NewsTips1()

    return render (request, 'index.html', {
        'form':     form,
        'message':  message,
    })




'''
from django.views.generic import TemplateView
class IndexView (TemplateView):
    template_name = 'index.html'

    def get_context_data (self, **kwargs):
        ctx = super(IndexView, self).get_context_data (**kwargs)
        ctx.update (
            form1 = NewsTips1(),
        )
        return ctx
'''
