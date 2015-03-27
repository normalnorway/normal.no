from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.flatpages.models import FlatPage
from apps.content.models import Content as ContentBlock
from forms import PageEditForm

#EditBlockView
#EditPageView


class BlockEditView (UpdateView):
    model = ContentBlock
    fields = 'content',
    template_name = 'content/edit_block.html'

    def get_success_url (self):
        request = self.request
        messages.success (request, 'Teksten er lagret!')
        if request.POST.has_key ('save-and-stay'):
            return request.get_full_path()
        else:
            return request.GET.get ('back')



class PageEditView (UpdateView):
    model = FlatPage
    form_class = PageEditForm
    template_name = 'flatpages/edit.html'

    def _check_perm (self, user, pk):
        if user.has_perm ('flatpages.change_flatpage'):
            return True
        if user.has_perm ('flatpages.change_flatpage_gsf'):
            return pk in (25,26)
        return False

    def form_valid (self, form):
        messages.success (self.request, 'Siden er lagret')
        return super (PageEditView, self).form_valid (form)

    def dispatch (self, *args, **kwargs):
        request = args[0]
        pk = int(kwargs['pk'])
        if not self._check_perm (request.user, pk):
            raise PermissionDenied()
        return super (PageEditView, self).dispatch (*args, **kwargs)



# Generate JSON list of pages for TinyMCE's 'link_list'
from django.http import JsonResponse
from django.contrib.flatpages.models import FlatPage

def page_list_json (request):
    data = []
    for page in FlatPage.objects.only ('title', 'url'):
        if page.url.startswith ('/europa/'): continue
        data.append ({'title': page.title, 'value': page.url})
    return JsonResponse (data, safe=False)
