# -*- encoding: utf-8 -*-

from django import forms


class MemberForm (forms.Form):
    name = forms.CharField (label=u'Navn', max_length=64)
    born = forms.DateField (label=u'Fødselsdato',
        input_formats = ('%d.%m.%y', '%d/%m/%y', '%d%m%y'),
        error_messages = {'invalid': u'Ugyldig dato. Bruk dd/mm/åå eller dd.mm.åå'})
    address1 = forms.CharField (label=u'Adresse')
    address2 = forms.CharField (label=u'Adresse', required=False)
    zipcode = forms.CharField (label=u'Postnummer', max_length=4)
    city = forms.CharField (label=u'Sted', max_length=64)
    phone = forms.CharField (label=u'Telefon', max_length=15, required=False)
    email = forms.EmailField (label=u'E-post', required=False)
    comment = forms.CharField (label=u'Kommentar', required=False,
                  widget=forms.Textarea (attrs=dict(rows=8, cols=70)))
