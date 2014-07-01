# -*- encoding: utf-8 -*-

from django import forms


CHOICES = (
    ('1', u'Nedkriminalisere cannabis (Portugal-modellen)'),
    ('2', u'Avkriminalisere cannabis for de over 18 år'),
    ('3', u'Avkriminalisere cannabis for de over 20 år'),
    ('4', u'Regulere cannabis. Staten tar seg av produksjon og distribusjon'),
)


MEMBER_CHOICES = (
    ('1', u'JA! Jeg ønsker å bli medlem og betale kr 100,- pr år'),
    ('2', u'JA! Jeg ønsker å bli oppført som støttemedlem uten kostnad'),
    ('3', u'JA! Jeg ønsker å donere følgende beløp til Normals arbeid: _____'),
)

EXTRA_CHOICES = (
    ('1', u'Jeg ønsker å være et aktivt medlem'),
    ('2', u'Jeg kan være kontaktperson for området jeg bor i'),
    ('3', u'Send meg informasjonsmateriell'),
    ('4', u'Jeg kan hjelpe til med å skrive'),
    ('5', u'Jeg kan hjelpe til med IT'),
)



class PetitionForm (forms.Form):
    choice =    forms.ChoiceField (label=u'Jeg ønsker å', required=True,
                                   widget=forms.RadioSelect, choices=CHOICES)
    name =      forms.CharField (label=u'Navn', max_length=64, required=True)
    city =      forms.CharField (label=u'Sted', max_length=64, required=True)
    public =    forms.BooleanField (label=u'Vis mitt navn')



class MemberForm (forms.Form):
    error_css_class = 'xerror'  # formerror, validation_error
    required_css_class = 'required'

    choice =    forms.ChoiceField (label='Type medlemskap', required=True,
                                   widget=forms.RadioSelect,
                                   choices=MEMBER_CHOICES)

    name =      forms.CharField (label=u'Navn', max_length=64)
    born =      forms.DateField (label=u'Fødselsdato',
                    input_formats = ('%d.%m.%y', '%d/%m/%y', '%d%m%y'),
                    error_messages = {'invalid': u'Ugyldig dato. Bruk dd/mm/åå eller dd.mm.åå'})
    address1 =  forms.CharField (label=u'Adresse')
    address2 =  forms.CharField (label=u'Adresse', required=False)
    zipcode =   forms.CharField (label=u'Postnummer', max_length=4)
    city =      forms.CharField (label=u'Sted', max_length=64)
    phone =     forms.CharField (label=u'Telefon', max_length=15, required=False)
    email =     forms.EmailField (label=u'E-post', required=False)
    comment =   forms.CharField (label=u'Kommentar', required=False,
                    widget=forms.Textarea (attrs=dict(rows=8, cols=70)))
    extra =     forms.MultipleChoiceField (label=u'Jeg kan bidra med',
                                           required=False,
                                           widget=forms.CheckboxSelectMultiple,
                                           choices=EXTRA_CHOICES)

    def clean_born (self):
        import datetime
        born = self.cleaned_data['born']
        if 18 > (((datetime.date.today() - born).days + 1) / 365):
            raise forms.ValidationError (u'Du må være fyllt 18 år for å melde deg inn!')

    # self.email.lower().strip()

#    def __init__ (self, *args, **kwargs):
#        super (MemberForm,self).__init__ (*args, **kwargs)
#        self.label_suffix = ''
#        self.initial = dict (name='Frode', phone='12345678')

#    def clean (self):
#        cleaned_data = super (MemberForm, self).clean()
#        return cleaned_data # not needed after django 1.7
