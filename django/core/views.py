from django.shortcuts import render, redirect
from core.shortcuts import render_to
from apps.content.models import get_content_dict


@render_to ('index.html')
def index (request):
    return get_content_dict ('forside')


@render_to ('newsletter.html')
def newsletter (request):
    return {}


# Note: Only used for testing. Do not remove.
@render_to ('test.html')
def test (request):
    return {}
