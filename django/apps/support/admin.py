from django.contrib import admin
from .models import Petition

class PetitionAdmin (admin.ModelAdmin):
    list_display = 'date', 'name', 'city', 'choice'
    #list_editable = 'name', 'city',
    list_display_links = 'choice',
    list_display_links = 'date', 'name',
    ordering = '-date', # @todo move to model: class Meta: get_latest_by = 'date'
                        #       so it's active for view
    search_field = 'name', 'city'
    list_filter = 'public', 'date', 'choice',
    #date_hierarchy = 'date'


admin.site.register (Petition, PetitionAdmin)
