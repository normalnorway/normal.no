"""
Import old data into apps.cms
flatpages -> Page
apps.content.Content -> Content
"""

from django.contrib.flatpages.models import FlatPage
from apps.content.models import Content as OldContent
from apps.cms.models import Page, Content


#Page.objects.all().delete()
#Content.objects.all().delete()


def init_content ():
    data = OldContent.objects.values ('pk', 'name', 'content')
    Content.objects.bulk_create (Content(**item) for item in data)


def init_page ():
    lst = FlatPage.objects.values('pk', 'title', 'url', 'content')
    for obj in lst: _transform_page_obj (obj);
    Page.objects.bulk_create (Page(**item) for item in lst)


def _transform_page_obj (obj):    # strip /sider/ prefix
    if obj['url'].startswith ('/sider/'):
        obj['url'] = obj['url'][7:]


if __name__ == '__main__':
    init_content()
    init_page()
