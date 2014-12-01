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
    return {}
