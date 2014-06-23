# encoding: utf-8

WELCOME_MSG = u'''
Velkommen som medlem og takk for støtten! Du vil i løpet av få dager mota
en giro per e-post eller brev.
'''

import os
import json
import datetime
from django.shortcuts import redirect
from django.contrib import messages
from core.shortcuts import render_to
from apps.content.models import get_content_dict
from .forms import MemberForm

from website.settings import BASE_DIR
member_fp = open (os.path.join (BASE_DIR, 'db', 'newmembers'), 'a+')

#welcome_msg = get_content ('innmelding-ferdig') # @todo must be short!


@render_to ('support:index.html')
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
    return ctx
