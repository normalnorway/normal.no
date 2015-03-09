# -*- encoding: utf-8 -*-
from django import forms

# tmp hack to allow norwegian month names
import locale
locale.setlocale (locale.LC_TIME, 'nb_NO.utf8')

# Note: http://www.korrekturavdelingen.no/K4datoaar.htm says never
# use slash to separate elements!
DATETIME_INPUT_FORMATS = [
    '%d/%m/%Y', '%d/%m/%y',     # 24/12/2015, 24/12/15
    '%d.%m.%Y', '%d.%m.%y',     # 24.12.2015, 24.12.15
    '%Y-%m-%d',                 # 2005-12-24
    '%d. %B %Y', '%d. %b %Y',   # 24. desember 2015, 24. des. 2015
]
DATETIME_INPUT_FORMATS += [s+' %H:%M' for s in DATETIME_INPUT_FORMATS]


# /nyheter/auto-ny/
class AutoNewForm (forms.Form):
    date = forms.DateTimeField (label='Dato (og helst tid)', required=False,
                                help_text='Når artikkelen er publisert. (De vanligste datoformat godtas.)',
                                input_formats = DATETIME_INPUT_FORMATS,
                                error_messages = {'invalid': u'Ugyldig dato eller datoformat. Bruk f.eks. "24.12.2015 16:20" eller "24.12.2015".'})
                                #error_messages = {'invalid': u'Ugyldig dato. Bruk f.eks. "dd.mm.åååå tt:mm" eller "åååå-mm-dd tt:mm"'})
    title = forms.CharField (label='Overskrift', required=False, max_length=128)
    summary = forms.CharField (label='Ingress', required=False, widget=forms.Textarea)
    # Hidden fields
    url = forms.URLField (label='Adresse (URL)', widget=forms.HiddenInput())
    image_url = forms.URLField (required=False, widget=forms.HiddenInput())
    url_is_canonical = forms.BooleanField (required=False, widget=forms.HiddenInput())
