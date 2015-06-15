from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView, FormView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Page, File
from .forms import FileCreateForm


# @todo can use CreateView instead?, since all magic happens on the model
class FileCreate (FormView):
    form_class = FileCreateForm
    #template_name = 'file/add.html'
    template_name = 'cms/file/add.html'

    def form_valid (self, form):
        #obj.save() enough?
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



# --------------
#   Page Views
# --------------

class PageDetail (DetailView):  # not in use
    model = Page


class PageList (ListView):      # needed?
    model = Page
    # template_name = cms/page_list.html


class PageUpdate (UpdateView):  # @todo acl
    model = Page
    fields = 'title', 'content',
    template_name_suffix = '_update'


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
