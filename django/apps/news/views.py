from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
#from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
#from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from models import Article
from forms import AutoNewForm

import logging
logger = logging.getLogger (__name__)


def _remove_empty (data):
    """Remove empty values from a dict. A copy is returned"""
    return dict((k, v) for k, v in data.iteritems() if v)

def _have_keys (data):
    #keys = {'url', 'title', 'summary', 'image', 'date'}    # python 2.7
    keys = set(('url', 'title', 'summary', 'image', 'date'))
    return keys.intersection (set(data.keys()))



import urlparse
from django.http import HttpResponse    # tmp
from django.views.generic import View
from newsgrab import get_metadata as get_opengraph_data

# TODO
# save user in article object
# add some logging
# try to clean up adress. but keep fragment?
#   urlparse.urlunparse(urlobj[:3] + ('',)*3)  # shall return same as url
#   url = 'http://netloc/path;parameters?query=argument#fragment'
#   url, fragment = urldefrag(original)
# clean up image_url? (strip query&fragment)
# check that url returns 200
# HEAD -S http://normal.no/bli-medlem
# warn user if not norwegian article?

class NewArticleView (View):
    """
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

    # Article can not be posted if some of these fields are missing.
    _required_fields = set(('url', 'date', 'title', 'summary', 'image_url'))

    @staticmethod
    def _get_metadata (url):
        """Get OpenGraph metadata for url"""
        urlobj = urlparse.urlsplit (url)
        if not urlobj.netloc.endswith ('.no'): return {}
        meta = get_opengraph_data (url)
        meta.pop ('type', None)
        meta.pop ('site_name', None)
        if meta.has_key (u'description'):
            meta[u'summary'] = meta.pop (u'description', u'')
        if meta.has_key ('image'):
            meta['image_url'] = meta.pop('image')
        if meta.has_key ('url'): # OG specs. says this is the canonical url
            meta['url_is_canonical'] = True
        else:
            meta['url'] = url
        return meta
        #return meta if meta else {} # why not just return meta?

    @staticmethod
    def _get_missing_fields (data):
        """Return set of missing metadata fields"""
        return NewArticleView._required_fields - set(data.keys())


    def get (self, request):
        url = request.GET.get ('url', '').strip()
        if not url:
            return render (request, self.template_name, dict(url_missing=True))
        return HttpResponse ('fixme')


    def post (self, request):
        url = request.POST.get ('url', '').strip()
        if not url: return HttpResponse ('Invalid usage!') # @todo raise
        return self._handle (url)

#        form = AutoNewForm (request.POST)
#        if not form.is_valid():
#            return render (request, self.template_name, dict(form=form))
#        return self._save_and_redirect (form.cleaned_data)


    def _handle (self, url):
        if Article.objects.filter (url=url).exists():
            return self._have_it()

        data = self._get_metadata (url)

        # If url and data[url] differ, must check both
        if data.has_key ('url') and url != data['url']:
            if Article.objects.filter (url=data['url']).exists():
                return self._have_it()

        if not self._get_missing_fields (data):
            return self._save_and_redirect (data) # pass have_all_fields?

        return HttpResponse ('break')

        form = AutoNewForm (initial=data)
        # @todo mark missing fields with css class?
        #self._fix_form (form, data) # xxx
        return render (request, self.template_name, dict(form=form, missing=True))
        #return self.render (dict(form=form, missing=True))


    def _have_it (self):
        messages.warning (self.request, u'Denne lenken har vi allerede i arkivet.')
        return redirect ('news-new')

    def _save_and_redirect (self, data):
        #return HttpResponse ('save aborted')
        self._save (data)
        title = data['title'] if data.has_key('title') else data['url']
        messages.success (self.request, u'Takk for nyhetstipset: ' + title)
        return redirect ('news-new')

    # Note: Article.published only true if validation passes and user
    # has the add_article permission.
    def _save (self, data):
        obj = Article (**data)
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

#    def _fix_form (self, form, data):
#        for key in _have_keys (data):
#            if form.fields.has_key (key):
#                form.fields[key].widget.attrs['readonly'] = True





from django.views.generic.detail import DetailView
from django.views.generic import ArchiveIndexView
from django.views.generic import YearArchiveView, MonthArchiveView

class ArticleDetailView (DetailView):   # rename DetailArticleView?
    """http://normal.no/nyheter/<pk>/"""
    def get_queryset (self): return Article.pub_objects


class ArchiveView (ArchiveIndexView):
    date_field = 'date'
    paginate_by = 25
    def get_queryset (self): return Article.pub_objects


# @todo show months in reversed order?
# @todo pagination
class YearView (YearArchiveView):
    date_field = 'date'
    make_object_list = True # False => only generate month list
    def get_queryset (self): return Article.pub_objects


class MonthView (MonthArchiveView):
    date_field = 'date'
    month_format = '%m'
    make_object_list = True
    def get_queryset (self): return Article.pub_objects
