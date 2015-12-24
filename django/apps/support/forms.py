# -*- encoding: utf-8 -*-

from django import forms
from models import Petition

# TODO:
#
# Make paying member the default choice
#
# MemberForm.name validate: two words, so people don't just
# write their first name. Or use two fields?
#
# https://normal.no/bli-medlem/
# hva innebærer det å være aktiv. bunntekst
#
# Validate zipcode on MemberForm (change type to int?). Someone wrote: u' 936'
# Probably because field has max_length=4 and therefore
# can only write 4 chars in the form. If the first char is
# a space, then the fourth char is silently ignored.
# Can use min_length=4 but it will probably accept spaces, so
# need manual validation.


class PetitionForm (forms.ModelForm):
    choice = forms.ChoiceField (label=u'Jeg ønsker å', required=True,
                                widget=forms.RadioSelect, choices=Petition.CHOICES)

    # @todo move cleaning stuff to the model?
    def clean_name (self):
        if len(self.cleaned_data['name'].split()) == 1:
            raise forms.ValidationError('not used') # u'Du må oppgi både fornavn og etternavn.
        return self.cleaned_data['name'].strip().title()

    def clean_city (self):
        return self.cleaned_data['city'].strip().title()


    class Meta:
        model = Petition
        fields = 'choice', 'name', 'city', 'public'

        #widgets = dict (choice=forms.RadioSelect)  # got extra "----" choice
        # xxx do not work when we override, like 'choice' above / only work when using fields from the model
        #labels = { 'choice': u'Modell. Jeg ønsker å', }
        #error_messages = {
        #    'choice': { 'required': 'Hello world', },
        #}



# MemberEnrollmentForm
class MemberForm (forms.Form):
    '''
    # better to put on the model. but no model for Member
    PAYING = '1'
    SUPPORTER = '2' # better? ASSOCIATE = '2'
    MEMBER_TYPE = (
        (PAYING, u'JA! Jeg ønsker å bli medlem og betale kr 100,- pr år.'),
        (SUPPORTER, '2', u'JA! Jeg ønsker å bli oppført som støttemedlem uten kostnad.'),
    )
    '''

    MEMBER_TYPE = (
        ('1', u'JA! Jeg ønsker å bli medlem og betale kr 100,- pr år.'),
        ('2', u'JA! Jeg ønsker å bli oppført som støttemedlem uten kostnad.'),
        #('3', u'JA! Jeg ønsker å donere følgende beløp til Normals arbeid: _____'),
        #  stottemedlem, men gi gave nå?
    )

    EXTRA_CHOICES = (
        ('1', u'Jeg ønsker å være et aktivt medlem.'),
        ('2', u'Jeg kan være kontaktperson for området jeg bor i.'),
        ('3', u'Send meg informasjonsmateriell.'),
        ('4', u'Jeg kan hjelpe til med å skrive.'),
        ('5', u'Jeg kan hjelpe til med IT.'),
        # @todo add to e-mail list? add to sms-list
    )

    choice =    forms.ChoiceField (label='Type medlemskap', choices=MEMBER_TYPE,
                                   widget=forms.RadioSelect)
    name =      forms.CharField (label=u'Navn', max_length=64)
    born =      forms.DateField (label=u'Fødselsdato',
                    widget = forms.TextInput (attrs={'placeholder': u'dd.mm.åååå'}),
                    input_formats = ('%d.%m.%y', '%d/%m/%y', '%d%m%y', '%d.%m.%Y', '%d/%m/%Y', '%d%m%Y'),
                    error_messages = {'invalid': u'Ugyldig fødselsdato. Bruk formatet dd.mm.åååå eller dd/mm/åååå'})
    address1 =  forms.CharField (label=u'Adresse')
    address2 =  forms.CharField (label=u'Adresse (ekstra)', required=False)
    zipcode =   forms.CharField (label=u'Postnummer', max_length=4)
    #zipcode =   forms.IntegerField (label=u'Postnummer', max_value=9999, min_value=???)    # better to accept any string, then use custom zipcode validator?
    city =      forms.CharField (label=u'Sted', max_length=64)
    phone =     forms.CharField (label=u'Telefon', max_length=15, required=False)
    email =     forms.EmailField (label=u'E-post', required=False)
    comment =   forms.CharField (label=u'Kommentar', required=False, widget=forms.Textarea (attrs={'rows': 8, 'cols': 70}))
    extra =     forms.MultipleChoiceField (label=u'Jeg kan bidra med',
                                           required=False,
                                           widget=forms.CheckboxSelectMultiple,
                                           choices=EXTRA_CHOICES)

    def clean_born (self):
        import datetime
        born = self.cleaned_data['born']
        cutoff = datetime.date (born.year+18, born.month, born.day)
        if cutoff > datetime.date.today():
            raise forms.ValidationError (u'Du må være fyllt 18 år for å melde deg inn!')
        return born
