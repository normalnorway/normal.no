from django.contrib import admin
from .models import Petition

class PetitionAdmin (admin.ModelAdmin):
    list_display = 'date', 'name', 'city', 'choice'
    list_filter = 'public', 'date', 'choice',
    #list_editable = 'name', 'city',
    list_display_links = 'choice',
    list_display_links = 'date', 'name',
    search_field = 'name', 'city'
    #date_hierarchy = 'date'


admin.site.register (Petition, PetitionAdmin)
