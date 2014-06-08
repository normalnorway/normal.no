# -*- encoding: utf-8 -*-

from django import forms

# @todo own forms.Field
#from core.forms import TextField

# Note: required=True is default for form fields

class NewsTips1 (forms.Form):
    url = forms.URLField (label='Adresse (url)')
    #url = forms.CharField (label='Lenke (URL)', max_length=64)

class NewsTips2 (forms.Form):
    date = forms.DateField (label='Dato',
                            #help_text=u'dd/mm/åå eller åååå-mm-dd',
                            input_formats = ('%Y-%m-%d', '%d/%m/%y', '%d. %A %Y'),
                            error_messages = {'invalid': u'Ugyldig dato. Bruk dd/mm/åå eller åååå-mm-dd'})
    #date = forms.DateField (label='Dato', help_text='Datoen artikkelen er publisert')
    title = forms.CharField (label='Overskrift', max_length=128)
    summary = forms.CharField (label='Ingress', widget=forms.Textarea)



class SearchForm (forms.Form):
    query = forms.CharField (max_length=100, label=u'Søk')
