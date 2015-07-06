# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User

# record activity. record date changed; then can list active/recent stuff

class Contact (models.Model):
    class Meta: ordering = 'name',
    name = models.CharField (max_length=64, unique=True)
    sted = models.CharField (max_length=64, blank=True, help_text='Where the person lives. City, etc.')
    phone = models.CharField (max_length=16, blank=True)
    phone2 = models.CharField (max_length=16, blank=True)
    email = models.EmailField (blank=True)
    email2 = models.EmailField (blank=True)
    facebook = models.URLField (blank=True) # initial='http://'
    company = models.CharField (max_length=64, blank=True, help_text='Company, organization, affiliation, etc.')
    notes = models.TextField (blank=True)
    tags = models.ManyToManyField ('ContactTag', blank=True)
    # sip, log, trust(a,b,c,d), a-laget?

    def __unicode__ (self):
        return self.name


class ContactTag (models.Model):
    class Meta: ordering = 'name',
    name = models.CharField (max_length=50)
    text = models.CharField (max_length=255, blank=True)
    def __unicode__ (self): return self.name


# --------------------------[ Task ]--------------------------


class Task (models.Model):
    class Meta: ordering = 'created',

    OPEN = '0'
    DONE = '1'
    STARTED = '2'

    PRIORITIES = (
        ('!', 'ASAP'),
        ('h', 'High'),
        ('m', 'Medium'),
        ('l', 'Low'),
    )
    STATES = (
        ('0', 'Not started'),
        ('1', 'Done'),
        ('2', 'Started'),
        ('3', 'Postponed'),
        ('4', 'Pending other'),
    )

    name = models.CharField (max_length=80) # title
    created = models.DateField (auto_now=True, editable=False)
    owner = models.ForeignKey (User, blank=True, null=True, help_text='Defaults to you')
    priority = models.CharField (max_length=1, default='m', choices=PRIORITIES)
    status = models.CharField (max_length=1, default='0', choices=STATES)
    #done = models.BooleanField (default=False)
    due = models.DateField (blank=True, null=True, help_text='Date the task should be complete')
    notes = models.TextField (blank=True)
    pending = models.ForeignKey ('Task', blank=True, null=True, help_text='Task awaits completion of other task')
    # TaskLog (what is done), started{date,bool}
    # length/time (estimate) <-- A: no, due is better
    # minor (easy/fast)
    # record involved contacts? (stifte lokallag?)

    def __unicode__ (self): return self.name


class SubTask (models.Model):   # TaskGoal
    '''Used to break a task into multiple sub-tasks or goals'''
    task = models.ForeignKey (Task)
    name = models.CharField (max_length=80)
    done = models.BooleanField (default=False)
    deadline = models.DateField (blank=True, null=True)
    assigned_to = models.ForeignKey (Contact, blank=True, null=True)
    notes = models.TextField (blank=True)
    # pending/depends other subtask
    def __unicode__ (self): return self.name


class TaskLog (models.Model):   # not in use
    '''Used to record work on a Task'''
    task = models.ForeignKey (Task)
    notes = models.TextField ()
    created = models.DateField (auto_now=True, editable=False)


# ------------------------[ Reminder ]------------------------

def _foobar (*args):
    return None

class Reminder (models.Model):
    # @type event, todo, meeting
    type = models.ForeignKey ('ReminderType')
    title = models.CharField (max_length=80)
    date = models.DateTimeField()   # start
    end = models.TimeField (blank=True, null=True, help_text='End time')
    location = models.CharField (max_length=80, blank=True)
    url = models.URLField (blank=True, help_text='e.g., link to facebook event')
    note = models.TextField (blank=True)
    alarm = models.IntegerField (blank=True, null=True, help_text='Set alarm to this many days before the event')
    task = models.ForeignKey (Task, blank=True, null=True, help_text='Link reminder to task')
    owner = models.ForeignKey (User, blank=True, null=True, help_text='Defaults to you')
    # important or priority
    # all_day_event. end->duration. recuring?
    # split note: (internal) notes and description (of seminar, e.g.)


class ReminderType (models.Model):
    class Meta: ordering = 'name',
    name = models.CharField (max_length=50)
    def __unicode__ (self): return self.name


# --------------------------[ Note ]--------------------------

class Note (models.Model):
    '''Short notes'''
    owner = models.ForeignKey (User, editable=False, blank=True, null=True)
    title = models.CharField (max_length=80, blank=True) # @todo drop?
    text = models.TextField (blank=True)
    # created, last_changed, task
    # @todo drop title and just show excerpt from text?
