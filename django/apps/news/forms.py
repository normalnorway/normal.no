# -*- encoding: utf-8 -*-
from django import forms

DATETIME_INPUT_FORMATS = (
    '%d/%m/%Y %H:%M', '%d/%m/%y %H:%M',
    '%d.%m.%Y %H:%M', '%d.%m.%y %H:%M',
    '%d. %B %Y %H:%M', '%d. %b %Y %H:%M',
    '%Y-%m-%d %H:%M',
    # 6. feb 2014, kl. 08:35
)


# /nyheter/auto-ny/
class AutoNewForm (forms.Form):
    date = forms.DateTimeField (label='Dato & tid', required=False,
                                help_text='Dato og tid artikkelen er publisert',
                                input_formats = DATETIME_INPUT_FORMATS,
                                error_messages = {'invalid': u'Ugyldig dato. Bruk f.eks. "dd.mm.åååå tt:mm" eller "åååå-mm-dd tt:mm"'})
    title = forms.CharField (label='Overskrift', required=False, max_length=128)
    summary = forms.CharField (label='Ingress', required=False, widget=forms.Textarea)
    # Hidden fields
    url = forms.URLField (label='Adresse (URL)', widget=forms.HiddenInput())
    image_url = forms.URLField (required=False, widget=forms.HiddenInput())
    url_is_canonical = forms.BooleanField (required=False, widget=forms.HiddenInput())
