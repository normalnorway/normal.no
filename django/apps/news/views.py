"""
BUGS:
- http://localhost:8000/nyheter/arkiv/2014/07/
  If no next month, then clicking "Neste maaned" fails
"""

from django.views.generic import dates
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
#from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Article
from .forms import AddNewForm, AutoNewForm
from .newsgrab import get_metadata


def _get_metadata (url):
    import urlparse
    urlobj = urlparse.urlparse (url)
    if not urlobj.netloc.endswith ('.no'):
        return {}   # only allow for norwegian sites
    data = get_metadata (url)   # @todo pass urlobj? urlobj=urlobj?
    return data if data else {}
    # @todo warn user if not norwegian
    # Note: og:url contains the canonical URL

def _remove_empty (data):
    """Remove empty values from a dict. A copy is returned"""
    return dict((k, v) for k, v in data.iteritems() if v)

def _get_missing (data): # rename _missing_keys
    keys = {'url', 'date', 'title', 'summary', 'image_url'}
    return keys - set(data.keys()) # note: returns a set

def _have_keys (data):
    keys = {'url', 'title', 'summary', 'image', 'date'}
    return keys.intersection (set(data.keys()))



from django.http import HttpResponse
from django.views.generic import View

class AutoNewView (View):
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

    template_name = 'news/add-new-auto.html'

    # TODO
    # try to clean up adress. but keep fragment?
    #   urlparse.urlunparse(urlobj[:3] + ('',)*3)  # shall return same as url
    # urlparse - urlsplit
    # check that url returns 200

    def get (self, request):
        url = request.GET.get ('url', '').strip()
        if not url: return HttpResponse ('missing parameters') # @todo raise

        if Article.objects.filter (url=url).exists():
            return self._have_it()

        data = _get_metadata (url)
        print data
        if data.has_key ('url') and url != data['url']:
            if Article.objects.filter (url=data['url']).exists():
                return self._have_it()

        if data.has_key ('image'):
            data['image_url'] = data.pop('image')
        if data.has_key ('url'):
            data['url_is_canonical'] = True
        else:
            data['url'] = url

        missing = _get_missing (data)
        if not missing: return self._save_and_redirect (data)

        form = AutoNewForm (initial=data)
        # @todo mark missing fields with css class
        #self._fix_form (form, data) # xxx
        return render (request, self.template_name, dict(form=form, missing=True))
        #return self.render (dict(form=form, missing=True))


    def post (self, request):
        form = AutoNewForm (request.POST)
        if not form.is_valid():
            return render (request, self.template_name, dict(form=form))
        return self._save_and_redirect (form.cleaned_data)


    def _have_it (self):
        messages.warning (self.request, u'Denne lenken har vi allerede i arkivet.')
        return redirect ('news-new')

    def _save_and_redirect (self, data):
        self._save (data)
        title = data['title'] if data['title'] else data['url']
        messages.success (self.request, u'Takk for nyhetstipset: "%s"' % title)
        return redirect ('news-new')

    def _save (self, data):
        obj = Article (**data)
        if not self.request.user.has_perm ('news.add_article'):
            obj.published = False
#        missing = _get_missing (_remove_empty (data))
#        if missing.intersection ({'date', 'title', 'summary'}):
#            obj.published = False   # required fields to publish
        try:
            obj.full_clean()
        except ValidationError as ex:   # @todo forms.ValidationError
            obj.published = False # with this can drop intersection test
        obj.save()

    def _fix_form (self, form, data):
        for key in _have_keys (data):
            if form.fields.has_key(key):
                form.fields[key].widget.attrs['readonly'] = True



# q: login_url='/loginpage/'
#@permission_required ('news.add_article')
def add_new (request):
    assert request.method != 'POST'
    return render (request, 'news/add-new.html')
    #return HttpResponse ('hello!')



def detail (request, news_id):
    """http://normal.no/nyheter/<pk>/"""
    return render (request, 'news/detail.html', {
        'item': get_object_or_404 (Article, pk=news_id, published=True)
        # @todo use same name as DetailView uses. (object?)
    })



class ArchiveView (dates.ArchiveIndexView):
    date_field = 'date'
    paginate_by = 25
    def get_queryset (self):
        return Article.pub_objects


# @todo show months in revered order?
# @todo pagination
class YearView (dates.YearArchiveView):
    date_field = 'date'
    make_object_list = True     # False => only generate month list
    def get_queryset (self):
        return Article.pub_objects


class MonthView (dates.MonthArchiveView):
    date_field = 'date'
    month_format = '%m'
    make_object_list = True
    def get_queryset (self):
        return Article.pub_objects
