from django.contrib import admin

# Customize flatpages
#from django.contrib.flatpages.models import FlatPage
#from django.contrib.flatpages.admin import FlatPageAdmin
#from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm


#class MyFlatPageAdmin(FlatPageAdmin):
#    form = FlatpageForm

#    class Media:
#        js = ('/media/j/jquery.js')
#        css = {'screen': ('/media/c/admin.css')}

#admin.site.unregister (FlatPage)
#admin.site.register (FlatPage, MyFlatPageAdmin)

# @todo remove site field, and hardcode it instead
# http://stackoverflow.com/questions/4786784/django-flatpages-default-site


'''
from django import forms

MY_CHOICES = ( 'foo', 'bar', 'baz' )

class MyFlatpageForm(FlatpageForm):
    template_name = forms.ChoiceField (choices=MY_CHOICES)

class MyFlatPageAdmin(FlatPageAdmin):
    form = MyFlatpageForm
'''
