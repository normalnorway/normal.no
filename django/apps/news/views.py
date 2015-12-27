# encoding: utf-8
"""
TODO NewsTip:
save user in article object
limit usage by ip for anonymous users
check that url returns 200
only allow http&https. not: javascript:alert(123)
try to clean up adress. but keep fragment?
  urlparse.urlunparse(urlobj[:3] + ('',)*3)  # shall return same as url
  url = 'http://netloc/path;parameters?query=argument#fragment'
  url, fragment = urldefrag(original)
clean up image_url? (strip query&fragment)
what about servers not responding? set timeout
HEAD -S http://normal.no/bli-medlem
"""

import logging
import urlparse
from django.http import HttpResponse    # tmp
from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from django.contrib import messages
from models import Article
from forms import NewArticleForm
from newsgrab import get_metadata as get_opengraph_data

logger = logging.getLogger (__name__)


class NewArticleView (View):
    """
    @todo outdated; update
    Sanity cheks:
    Check if url is (syntactically) valid
    Check if url exists (200, 30x)    Q: what if redirected?
    Check if we have url (move before exists check?)
    Check if norwegian url
    Try to fetch metadata
    If url!=canonical_url => check if we have canonical_url
    If all metadata is present => save and redirect
    Ask user to fill in missing metadata
    """

    template_name = 'news/article_new.html'

    _MSG_SUCCESS = u'Takk for nyhetstipset: %s'
    _MSG_HAVE_IT = u'Takk, men denne lenken har vi allerede i arkivet.'
    _MSG_FOREIGN = mark_safe (u'''
Nyhetsarkivet er for norske nyhetssaker. Lenken du sendte er til en
utenlandsk adresse. Hvis du fortsatt mener saken er relevant, send den
til <a href="mailto:post@normal.no">post@normal.no</a>. Takk!
''')

    # Article can not be published if some of these fields are missing.
    # @todo this list can be auto-build from required fields on Article
    _required_fields = set(('url', 'date', 'title', 'summary'))

    # Fields to copy from newsgrab into news.Article
    _all_fields = ('url', 'date', 'title', 'image_url', 'summary', 'url_is_canonical')

    @staticmethod
    def _get_metadata (url):
        """Get OpenGraph metadata for url"""
        urlobj = urlparse.urlsplit (url)
        if not urlobj.netloc.endswith ('.no'): return {}
        meta = get_opengraph_data (url)
        if meta.has_key (u'description'):
            meta[u'summary'] = meta.pop (u'description', u'')
        if meta.has_key ('image'):
            meta['image_url'] = meta.pop('image')
        if meta.has_key ('url'): # OG specs. says this is the canonical url
            meta['url_is_canonical'] = True
        else:
            meta['url'] = url
        return meta

    def _get_missing_fields (self, data):
        """Return set of missing metadata fields"""
        return self._required_fields - set(data.keys())


    def get (self, request):
        url = request.GET.get ('url', '').strip()
        if not url: return render (request, self.template_name, {})
        return self._handle (url)


    def post (self, request):
        if request.POST.get ('step2', False):
            form = NewArticleForm (request.POST)
            if not form.is_valid():
                return render (request, self.template_name, dict(form=form))
            return self._save_and_redirect (form.cleaned_data)

        # Step 1: Collect URL
        url = request.POST.get ('url', '').strip()
        if not url: return HttpResponse ('Invalid usage!') # @todo raise
        return self._handle (url)


    # post() and get() delegates to this method
    def _handle (self, url):
        if Article.objects.filter (url=url).exists():
            return self._have_it()

        # Q: howto get http status code from newsgrab
        # Q: howto get redirect info. needed?
        from urllib2 import HTTPError, URLError   # tmp hack
        try:
            data = self._get_metadata (url)
        except (HTTPError, URLError) as ex:
            # @todo better to report as form error
            messages.error (self.request, 'Kan ikke åpne lenken: %s' % ex.reason)
            return redirect ('news-new')
        if not data:
            messages.info (self.request, self._MSG_FOREIGN)
            #messages.warning (self.request, self._MSG_FOREIGN) # warnings are shown in red; so are the links
            return redirect ('news-new')

        # If url and data[url] differ, must check both
        if data.has_key ('url') and url != data['url']:
            if Article.objects.filter (url=data['url']).exists():
                return self._have_it()

        if not self._get_missing_fields (data):
            return self._save_and_redirect (data) # pass have_all_fields?

        # Ask user to fill in missing data
        form = NewArticleForm (initial=data)
        # @todo don't allow anonymous users to change prefilled fields?
#        for field in form.visible_fields():
#            if not field.value(): continue
#            form.fields[field.name].widget.attrs['readonly'] = True
#            #field.widget.attrs['readonly'] = True
        return render (self.request, self.template_name, dict(form=form))


    def _have_it (self):
        messages.warning (self.request, self._MSG_HAVE_IT)
        return redirect ('news-new')

    def _save_and_redirect (self, data):
        #return HttpResponse ('save aborted')
        self._save (data)
        title = data['title'] if 'title' in data else data['url']
        messages.success (self.request, self._MSG_SUCCESS % (title,))
        return redirect ('news-new')

    # Note: Article.published only true if validation passes and user
    # has the add_article permission.
    def _save (self, data):
        newdata = { key: data[key] for key in data if key in self._all_fields }
        obj = Article (**newdata)
        try:
            obj.full_clean()
        except ValidationError as ex:
            logger.warn ('ValidationError: setting published=False for: ' + obj.url)
            logger.warn ('    Why: ' + str(ex))
            obj.published = False
        if not self.request.user.has_perm ('news.add_article'):
            logger.warn ('Add permission missing: setting published=False for: ' + obj.url)
            obj.published = False
        obj.save()




from django.views.generic.detail import DetailView
from django.views.generic import ArchiveIndexView
from django.views.generic import YearArchiveView, MonthArchiveView

class ArticleDetailView (DetailView):   # rename DetailArticleView?
    """http://normal.no/nyheter/<pk>/"""
    def get_queryset (self):
        return Article.pub_objects


class OnlyPublishedMixin (object):
    def get_queryset (self):
        return Article.pub_objects.order_by ('-date')


# self: model, object_list, options, queryset, request
# Combine mixins
#class OnlyPublishedMixin (_OnlyPublishedMixin, CacheMixin):
#    pass


# Not using Djangos generic date view since date_list is not lazily evaluated
#class ArchiveView (OnlyPublishedMixin, ArchiveIndexView):
#    date_field = 'date'
#    paginate_by = 50
#    allow_empty = True
    #allow_future = True    # ~50% faster sql query

# Create own archive view that does lazy evaluation on date_list
from django.views.generic.list import ListView
class ArchiveView (OnlyPublishedMixin, ListView):
    template_name = 'news/article_archive.html'
    paginate_by = 50
    allow_empty = True
    def get_context_data (self, **kwargs):
        ctx = super (ArchiveView,self).get_context_data (**kwargs)
        ctx['date_list'] = Article.objects.dates ('date', 'year', order='DESC')
        return ctx
#    def date_list (self):  # shorter. but can't emulate ArchiveIndexView 100%
#        return Article.objects.dates ('date', 'year', order='DESC')


# @todo show months in reversed order?
class YearView (OnlyPublishedMixin, YearArchiveView):
    date_field = 'date'
    make_object_list = True   # generate month list *and* object list


class MonthView (OnlyPublishedMixin, MonthArchiveView):
    date_field = 'date'
    month_format = '%m'
    make_object_list = True
