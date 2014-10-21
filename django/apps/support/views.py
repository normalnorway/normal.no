# encoding: utf-8

WELCOME_MSG = u'''
Velkommen som medlem og takk for støtten! Du vil i løpet av én uke motta
en velkomst e-post. Betalende medlemmer vil også få en giro per e-post.
'''

PETITION_MSG = u'''
Takk for at du skrev deg på oppropet! Sammen kan vi legge press på
myndigheter og styrende organer. Oppfordr gjerne andre til å gjøre det
samme ved å dele lenke til denne siden.
'''

import os
import datetime
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib import messages
from django.core.cache import cache
from core.shortcuts import render_to
from apps.content.models import get_content, get_content_dict

from . import add_new_member
#import member  # then can do: member.add(...)
from .models import Petition
from .forms import MemberForm, PetitionForm

# Key is model char, value is get_choice_display(char)
CHOICE_DISPLAY = dict(Petition.CHOICES)


def get_petition_stats (data):
    '''Calculate and cache statistics for the petition'''
    ckey = 'support-petition-stats'
    stats = cache.get (ckey)
    if stats: return stats

    stats = dict()
    count = data.count()

    model_stats = []
    for item in Petition.objects.values_list ('choice').annotate(Count('id')).order_by('-id__count'):
        model_stats.append ({
            'model':    CHOICE_DISPLAY[item[0]],
            'percent':  int (round(100*float(item[1])/count)),
        })
    stats['model'] = model_stats
    stats['city'] = Petition.objects.values ('city').annotate(Count('id')).order_by('-id__count')[0:5]
    stats['week'] = count * 7 / (Petition.objects.latest().date - Petition.objects.earliest().date).days
    stats['last_week'] = data.filter (date__gt = datetime.datetime.now() - datetime.timedelta(days=7)).count()

    cache.set (ckey, stats)
    return stats



# @todo sanitize name
# @todo ask for full name
# @todo nuke stats in cache on new signup?
@render_to ('support:petition.html')
def petition (request):
    data = Petition.objects.all()
    ctx = {
        'objects':  data.filter (public=True)[0:50],
        'form':     PetitionForm(),
        'toptext':  get_content ('opprop-top'),
        'count':    data.count(),
        'stats':    get_petition_stats (data)
    }

    if not request.method == 'POST':
        return ctx

    form = PetitionForm (request.POST)
    if form.is_valid():
        obj = form.save()
        form = PetitionForm()   # clear the form
        messages.success (request, PETITION_MSG)
    ctx['form'] = form
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
        add_new_member (data)
        messages.success (request, WELCOME_MSG)
        ctx['form'] = MemberForm()  # clear the form

    return ctx
