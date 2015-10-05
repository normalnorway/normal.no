from django.contrib import messages
from django.utils.html import mark_safe
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import condition
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Page, Content, File


class FileSelect (ListView):
    model = File
    template_name_suffix = '_select'



# -----------------
#   Content Views
# -----------------

class ContentUpdate (UpdateView):
    model = Content
    fields = 'content',
    template_name_suffix = '_update'

    def get_success_url (self):
        messages.success (self.request, 'Teksten er lagret')
        return self.request.GET.get ('next', '/')



# ----------------
#    Page Views
# ----------------

class PageUpdate (UpdateView):
    model = Page
    fields = 'title', 'content',
    template_name_suffix = '_update'

    def form_valid (self, form):
        messages.success (self.request, 'Siden er lagret')
        return super (PageUpdate, self).form_valid (form)



def _page_last_modified (request, url):
    try: return Page.objects.get (url='/'+url, published=True).modified
    except Page.DoesNotExist:
        return None

@condition(last_modified_func=_page_last_modified)
def page (request, url):
    page = get_object_or_404 (Page, published=True, url = '/'+url)
    page.content = mark_safe (page.content)  # @todo do in HTMLField.__get__
    opengraph = {
        'title':        page.title + ' | Normal',
        'description':  page.summary,
        'image':        page.image.url if page.image else None,
    }
    return render (request, 'cms/page_detail.html', {'page': page, 'og': opengraph})



# Generate JSON list of pages for TinyMCE's 'link_list'
from django.http import JsonResponse

STATIC_PAGE_LIST = [
    {'title': 'Blogg',      'value': 'http://blogg.normal.no'},
    {'title': 'Facebook',   'value': 'https://www.facebook.com/NormalNorway'},
    {'title': 'Twitter',    'value': 'https://twitter.com/NormalNorway'},
    {'title': 'Youtube',    'value': 'http://www.youtube.com/user/normalnorway'},
    {'title': 'normal.no',  'menu': None},
]

# @todo convert sub paths into (sub) menu?
def page_list_json (request):
    data = []
    for page in Page.objects.only ('title', 'url'):
        if page.url.startswith ('/europa/'): continue
        data.append ({'title': page.title, 'value': page.url})
    L = STATIC_PAGE_LIST
    L[-1]['menu'] = data
    return JsonResponse (L, safe=False)
