# We use the login & logut view from the auth module.
# @see urls.py

from django.http import HttpResponseRedirect
from django.contrib import auth


def logout (request):
    if request.user.is_authenticated():
        auth.logout (request)
    return HttpResponseRedirect ("/")
