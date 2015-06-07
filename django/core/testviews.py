# encoding: utf-8
"""
Views used for testing while developing.
"""

#from pprint import pprint
#from django.http import HttpResponse
from core.shortcuts import render_to


@render_to ('test.html')
def test (request):
    from django.contrib import messages
    from django.utils.html import mark_safe
    messages.info (request, mark_safe('Send us an <a href="mailto:post@normal.no">email</a>!'))
    messages.warning (request, 'Hei på deg')
    messages.error (request, u'Hei på deg')
    return {}
    #return HttpResponse ('Testing')
