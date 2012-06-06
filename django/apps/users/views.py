from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required

#from apps.users import forms
from apps.users.models import Profile
from apps.users.forms import RegistrationForm


@login_required
def profile (request):
    return render (request, 'users/profile.html', { 'user': request.user })


def register (request):
#    form = auth.forms.UserCreationForm()
#    form = forms.NewUserForm()
    if request.method == "POST":
        form = RegistrationForm (request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            p = user.get_profile()
            p.country = form.cleaned_data['country']
            p.avatar = form.cleaned_data['avatar']
            # @todo resize&crop image
#            p.avatar = request.FILES['avatar']
            p.save()
            return HttpResponseRedirect ("/accounts/profile")
    else:
        form = RegistrationForm()

    return render (request, 'users/register.html', { 'form': form })



# Using django.contrib.auth.views.login instead. @see urls.py
#def login (request):


# @todo use auth.view instead and redirect with next_page=/
def logout (request):
    if request.user.is_authenticated():
        auth.logout (request)
    return HttpResponseRedirect ("/")
