# encoding: utf-8
import os
import json
import datetime
from django.shortcuts import redirect
from django.contrib import messages
from core.shortcuts import render_to
from apps.content.models import Content
from .forms import MemberForm

from website.settings import BASE_DIR
member_fp = open (os.path.join (BASE_DIR, 'db', 'newmembers'), 'a+')
#import codecs
#member_fp = codecs.open (os.path.join (BASE_DIR, 'db', 'newmembers'), 'a+', 'utf-8')

WELCOME_MSG = u'''
Velkommen som medlem og takk for støtten! Du vil i løpet av få dager mota
en giro per e-post eller brev.
'''


@render_to ('support:index.html')
def index (request):
    # sql in operator does not preserve order
    #top, bottom = Content.objects.filter (name__in=['innmelding-top', 'innmelding-bunn'])
    top     = Content.objects.get (name='innmelding-top')
    bottom  = Content.objects.get (name='innmelding-bunn')

    if not request.method == 'POST':
        return dict (form=MemberForm(label_suffix=''), top=top.content, bottom=bottom.content)
    form = MemberForm (request.POST, label_suffix='')
    if form.is_valid():
        data = form.cleaned_data
        data['born'] = data['born'].strftime ('%F') # json don't handle datetime
        data['enrolled'] = datetime.datetime.now().strftime('%F')
        # @todo filter/remove empty
        json.dump (data, member_fp)
        member_fp.write ('\n')
        member_fp.flush()
        messages.success (request, WELCOME_MSG)
#        form = MemberForm(label_suffix='')
    return dict (form=form, top=top.content, bottom=bottom.content)
