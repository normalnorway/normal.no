# encoding: utf-8

WELCOME_MSG = u'''
Velkommen som medlem og takk for støtten! Du vil i løpet av én uke motta
en velkomst e-post. Betalende medlemmer vil også få en giro per e-post.
'''

import os
import datetime
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib import messages
from core.shortcuts import render_to
from apps.content.models import get_content, get_content_dict

from . import add_new_member
from .models import Petition
from .forms import MemberForm, PetitionForm


# @todo sanitize name
# @todo make sure can't sign up twice (or just clear the form?)
# @todo ask for full name
@render_to ('support:petition.html')
def petition (request):
    L = Petition.objects.all()
    count = L.count()

    # Calculate some statistics
    # @todo when did pettition start; how many per week
    # @todo cache!
    # Petition.objects.values('choice').annotate(Count('id')).order_by()
    # Petition.objects.values_list('choice').annotate(Count('id')).order_by('-id__count')
    ctbl = dict(Petition.CHOICES) # @todo static
    stats = []
    for item in Petition.objects.values_list ('choice').annotate(Count('id')).order_by('-id__count'):
        stats.append ((item[0], item[1], ctbl[item[0]],
                      int(round(100*float(item[1])/count))))
        # 0: choice, count, get_choice_display, percent

    city_stats = []
    foo = Petition.objects.values ('city').annotate(Count('id')).order_by('-id__count')[0:5]

    ctx = {
        'count':    count,
        'objects':  L.filter (public=True)[0:50],
        'form':     PetitionForm(),
        'toptext':  get_content ('opprop-top'),
        'stats':    stats,
        'citystats': foo,
    }
    if not request.method == 'POST': return ctx
    form = PetitionForm (request.POST)
    if form.is_valid():
        obj = form.save()
        messages.success (request, u'Takk for at du skrev deg på oppropet! Få gjerne en bekjent til å gjøre det også.')
    else: ctx['form'] = form
    return ctx



@render_to ('support:enroll.html')
def index (request):
    ctx = get_content_dict ('innmelding-top', 'innmelding-bunn')
    if not request.method == 'POST':
        ctx['form'] = MemberForm()
        return ctx
    ctx['form'] = form = MemberForm (request.POST)
    if form.is_valid():
        data = form.cleaned_data
        data['enrolled'] = datetime.datetime.now().strftime('%F')
        json.dump (data, member_fp)
        member_fp.write ('\n')
        member_fp.flush()
        messages.success (request, WELCOME_MSG)
        ctx['form'] = MemberForm()  # clear form
    return ctx
