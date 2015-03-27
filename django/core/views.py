from core.shortcuts import render_to


@render_to ('index.html')
def index (request):
    return {}


@render_to ('newsletter.html')
def newsletter (request):
    return {}


# Note: Only used for testing. Do not remove.
#from pprint import pprint
def test (request):
    from django.http import HttpResponse
    return HttpResponse ('Testing')
