from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.edit import UpdateView, FormView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Page, Content, File
from .forms import FileCreateForm


# @todo can use CreateView instead?, since all magic happens on the model
class FileCreate (FormView):
    form_class = FileCreateForm
    #template_name = 'file/add.html'
    template_name = 'cms/file/add.html'

    def form_valid (self, form):
        #obj.save() enough? what does parent do?
        obj = form.save (commit=False)
        obj.full_clean()
        obj.save()
        # @todo save() might raise IntegrityError: UNIQUE constraint failed: cms_file.name
        # @todo message
        return redirect ('file-add')
        #return redirect ('cms:file-add') # u'cms' is not a registered namespace
        #return super(FileCreate, self).form_valid(form) # uses success_url


class FileSelect (ListView):
    model = File
    template_name_suffix = '_select'



# -----------------
#   Content Views
# -----------------

class ContentUpdate (UpdateView):  # @todo acl
    model = Content
    fields = 'content',
    template_name_suffix = '_update'

    def get_success_url (self):
        messages.success (self.request, 'Teksten er lagret')
        return self.request.GET.get ('next', '/')



# ----------------
#    Page Views
# ----------------

#class PageDetail (DetailView):
#    model = Page


#class PageList (ListView):
#    model = Page
    # template_name = cms/page_list.html


class PageUpdate (UpdateView):  # @todo acl
    model = Page
    fields = 'title', 'content',
    template_name_suffix = '_update'
    def form_valid (self, form):
        messages.success (self.request, 'Siden er lagret')
        return super (PageUpdate, self).form_valid (form)


# Used to map static urls to Page
class PageByUrl (DetailView):   # @todo inherit from View?
    model = Page
    url = None
    def get_object (self):
        return self.model.objects.get (url=self.url)


# Used to map /<prefix>/* to Page
def page (request, url):
    page = get_object_or_404 (Page, url=url)
    return render (request, 'cms/page_detail.html', {'page': page})
    # cms/page.html?


def page_europe_hack (request, url):
    url = '/europa/%s/' % url
    page = get_object_or_404 (Page, url=url)
    return render (request, 'cms/page_detail.html', {'page': page})


# Generate JSON list of pages for TinyMCE's 'link_list'
from django.http import JsonResponse

STATIC_PAGE_LIST = [
    {'title': 'Blogg',      'value': 'http://blogg.normal.no'},
    {'title': 'Facebook',   'value': 'https://www.facebook.com/NormalNorway'},
    {'title': 'Twitter',    'value': 'https://twitter.com/NormalNorway'},
    {'title': 'Youtube',    'value': 'http://www.youtube.com/user/normalnorway'},
    {'title': 'normal.no',  'menu': None},
]

def page_list_json (request):
    data = []
    for page in Page.objects.only ('title', 'url'):
        if page.url.startswith ('/europa/'): continue
        if page.url[0] != '/':
            page.url = '/sider/' + page.url # XXX don't hardcode prefix
        data.append ({'title': page.title, 'value': page.url})
    L = STATIC_PAGE_LIST
    L[-1]['menu'] = data
    return JsonResponse (L, safe=False)
