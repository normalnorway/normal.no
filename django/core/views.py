"""
Global views -- i.e., don't tied to any app or model.
"""

from core.shortcuts import render_to


@render_to ('index.html')
def index (request):
    return {}


@render_to ('newsletter.html')
def newsletter (request):
    return {}
