# encoding: utf-8

WELCOME_MSG = u'''
Velkommen som medlem og takk for støtten! Du vil i løpet av få dager mota
en giro per e-post eller brev.
'''
# @todo brev kommer ikke. oppfordre til å oppgi e-post

import os
import json
import datetime
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib import messages
from core.shortcuts import render_to
from apps.content.models import get_content, get_content_dict

from .models import Petition
from .forms import MemberForm, PetitionForm

# @todo move to __init__ ? NEW_MEMBERS_FILENAME? or get_filename,
# new_member_get_fp, new_member_add? NewMember.add?
from website.settings import ROOT_DIR
member_fp = open (os.path.join (ROOT_DIR, 'db', 'newmembers'), 'a')


# @todo sanitize name
# @todo make sure can't sign up twice (or just clear the form?)
# @todo ask for full name
@render_to ('support:petition.html')
def petition (request):
    L = Petition.objects.all().order_by('-date')
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
        data['born'] = data['born'].strftime ('%F') # json don't handle datetime
        data['enrolled'] = datetime.datetime.now().strftime('%F')
        # @todo filter/remove empty
        json.dump (data, member_fp)
        member_fp.write ('\n')
        member_fp.flush()
        messages.success (request, WELCOME_MSG)
        ctx['form'] = MemberForm()  # clear form
    return ctx
