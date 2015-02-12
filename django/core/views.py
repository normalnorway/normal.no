# @todo move to root ?
from core.shortcuts import render_to


@render_to ('index.html')
def index (request):
    return {}


@render_to ('newsletter.html')
def newsletter (request):
    return {}


# Note: Only used for testing. Do not remove.
@render_to ('test.html')
def test (request):
    from pprint import pprint
    #pprint (request.META)
    return { 'foo': request.GET.get('url') }
    #return { 'foo': request.META.get('HTTP_REFERER') }
