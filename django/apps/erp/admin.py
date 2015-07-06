from django.contrib import admin
from .models import Contact, ContactTag
from .models import Task, SubTask, Reminder, ReminderType, Note

#admin.site.register (Task)


@admin.register (Note)
class NoteAdmin (admin.ModelAdmin):
    list_display = 'title', 'owner'
    list_filter = 'owner',
    search_fields = 'title', 'text',
    # @todo show excerpt of text


# ------------------------[ Reminder ]------------------------

@admin.register (Reminder)
class ReminderAdmin (admin.ModelAdmin):
    ordering = 'date',
    list_display = 'type', 'title', 'date', 'end', 'location', 'alarm', 'owner', 'task',
    list_filter = 'type', 'owner', 'task',
    search_fields = 'title', 'location', 'note',
    date_hierarchy = 'date'
    # @todo filter: future, past, today?

    def save_model (self, request, obj, form, change):
        if not change and not obj.owner: # owner defaults to current user
            obj.owner = request.user
        obj.save()

admin.site.register (ReminderType)


# --------------------------[ Task ]--------------------------

class SubTaskInline (admin.TabularInline):
    model = SubTask
    fields = 'name', 'deadline', 'done', 'assigned_to',

@admin.register (Task)
class TaskAdmin (admin.ModelAdmin):
    list_display = 'name', 'owner', 'status', 'due', 'priority', 'pending',
    list_filter = 'owner', 'status', 'priority', 'pending',
    search_fields = 'name', 'notes',
    date_hierarchy = 'due'
    inlines = SubTaskInline,

@admin.register (SubTask)
class SubTaskAdmin (admin.ModelAdmin):
    list_display = 'task', 'name', 'done', 'deadline', 'assigned_to',
    list_filter = 'done', 'task', 'assigned_to', # q: task filter not shown
    search_fields = 'name', 'notes',
    #date_hierarchy = 'deadline'


# ------------------------[ Contact ]------------------------

# @todo phone+phone2 on same line

@admin.register (Contact)
class ContactAdmin (admin.ModelAdmin):
    list_display = 'name', 'phone', 'email', 'company',
    list_filter = 'tags',   # company?
    from django.forms import CheckboxSelectMultiple
    from django.db import models
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

@admin.register (ContactTag)
class ContactTagAdmin (admin.ModelAdmin):
    list_display = 'name', 'text',
