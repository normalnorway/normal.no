from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView
from .models import Page


def page (request, url):
    page = get_object_or_404 (Page, url=url)
    return render (request, 'cms/page.html', {'page': page})


class PageUpdateView (UpdateView):
    model = Page
    fields = 'content',
    template_name = 'cms/edit_page.html' # default: cms/page_form.html
    # q: make template name match view name?
#edit_page = login_required (PageUpdateView.as_view())
