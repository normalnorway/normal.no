# -*- encoding: utf-8 -*-
from django import forms


# /nyheter/ny/
# use modelform instead? then don't need own unique validation
class AddNewForm (forms.Form):
    url = forms.URLField (label='Adresse (URL)')
    date = forms.DateField (label='Dato',
                            help_text='(Datoen artikkelen er publisert)',
                            # @todo %d/%m/%Y
                            input_formats = ('%Y-%m-%d', '%d.%m.%Y', '%d.%m.%y', '%d/%m/%y', '%d. %B %Y'),
                            error_messages = {'invalid': u'Ugyldig dato. Bruk dd.mm.åå eller åååå-mm-dd'})
    title = forms.CharField (label='Overskrift', max_length=128)
    summary = forms.CharField (label='Ingress', widget=forms.Textarea)


#class AddNewForm1 (forms.Form):    # url
#class AddNewForm2 (AddNewForm1):   # date, title, summary
