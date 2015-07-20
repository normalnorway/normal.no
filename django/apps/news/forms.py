# coding: utf-8
from django import forms

# XXX tmp hack to allow norwegian month names
#import locale
#locale.setlocale (locale.LC_TIME, 'nb_NO.utf8')

# Note: http://www.korrekturavdelingen.no/K4datoaar.htm says never
# use slash to separate elements!
DATETIME_INPUT_FORMATS = [
    '%d/%m/%Y', '%d/%m/%y',     # 24/12/2015, 24/12/15
    '%d.%m.%Y', '%d.%m.%y',     # 24.12.2015, 24.12.15
    '%Y-%m-%d',                 # 2005-12-24
#    '%d. %B %Y', '%d. %b %Y',   # 24. desember 2015, 24. des. 2015
]
DATETIME_INPUT_FORMATS += [s+' %H:%M' for s in DATETIME_INPUT_FORMATS]
# @todo also allow dot as separator. e.g., "kl. 14.00" (sprakradet.no)


class NewArticleForm (forms.Form):
    date = forms.DateTimeField (label='Dato (og helst tid)', required=False,
        help_text='Når artikkelen er publisert. De vanligste datoformat godtas.',
        input_formats = DATETIME_INPUT_FORMATS,
        error_messages = {'invalid':
            u'Ugyldig dato. Bruk f.eks. «dd.mm.åååå» eller «åååå-mm-dd»'
        })
    title = forms.CharField (label='Overskrift', required=False, max_length=128)
    summary = forms.CharField (label='Ingress', required=False, widget=forms.Textarea)
    # hidden fields:
    url = forms.URLField (label='Adresse (URL)', widget=forms.HiddenInput())
    image_url = forms.URLField (required=False, widget=forms.HiddenInput())
    url_is_canonical = forms.BooleanField (required=False, widget=forms.HiddenInput())

    # can't use this to strip fields either.
    # date is NoneType if not parsable as valid date, else datetime obj
#    def clean (self):
#        data = self.cleaned_data
#        d = data.get ('date', None)
#        print type(d)
#        print d
#        #if d: data['date'] = data['date'].strip()
#        return data

    # looks like not called untill form validates
    # so can't use this to strip the form field
#    def clean_date (self):
#        date = self.cleaned_data['date']
#        return date
