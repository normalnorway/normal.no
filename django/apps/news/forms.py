# -*- encoding: utf-8 -*-
from django import forms


class SearchForm (forms.Form):
    query = forms.CharField (max_length=100, label=u'Søk') # @todo html5 type=search?



# NOT IN USE

class NewsTipsStep1 (forms.Form):
    url = forms.URLField (label='Adresse (url)')
    #url = forms.CharField (label='Lenke (URL)', max_length=64)

class NewsTipsStep2 (forms.Form):
    date = forms.DateField (label='Dato',
                            #help_text=u'dd/mm/åå eller åååå-mm-dd',    # @todo html5 placeholder?
                            input_formats = ('%Y-%m-%d', '%d/%m/%y', '%d. %B %Y'),
                            error_messages = {'invalid': u'Ugyldig dato. Bruk dd/mm/åå eller åååå-mm-dd'})
    #date = forms.DateField (label='Dato', help_text='Datoen artikkelen er publisert')
    title = forms.CharField (label='Overskrift', max_length=128)
    summary = forms.CharField (label='Ingress', widget=forms.Textarea)
