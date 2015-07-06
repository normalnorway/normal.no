import datetime, calendar
from django import template
from apps.erp.models import Task, Reminder, Note
#from django.utils.safestring import mark_safe
from .utils import MyCalendar
from .utils import DateMarks

register = template.Library()

# @todo override HTMLCalendar.formatday
# http://stackoverflow.com/a/1458077

#mycal = calendar.LocaleHTMLCalendar (locale='nb_NO.utf8') # not thread-safe
#mycal = calendar.HTMLCalendar ()

# http://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/




@register.simple_tag
def erp_cal ():
    today = datetime.date.today()
    dmin = today.replace (day=1)
    try:
        dmax = dmin.replace (month = dmin.month+3)
    except ValueError:
        dmax = dmin.replace (month = dmin.month+3-12, year=dmin.year+1)
#    print dmin, dmax

    marks = DateMarks()
    marks.add (today, 'Today', csscls=['today'], url='http://normal.no')

    for obj in Reminder.objects.filter (date__gte=dmin, date__lt=dmax):
        marks.add (obj.date, obj.title, csscls=[obj.type.name])
    for obj in Task.objects.filter (due__gte=dmin, due__lt=dmax):
        marks.add (obj.due, obj.name, csscls=['task'])
    # url=reverse(obj.pk)

    # add (dateobj, title='', csscls=None)

    mycal = MyCalendar (marks)
#    html  = mycal.formatmonth (now.year, now.month-1, withyear=False)
    html = ''
    html += mycal.formatmonth (today.year, today.month,   withyear=False)
    html += mycal.formatmonth (today.year, today.month+1, withyear=False)
    html += mycal.formatmonth (today.year, today.month+2, withyear=False)
    return html
    #return mark_safe (html)




@register.assignment_tag
def erp_get_tasks (user=None):
    qs = Task.objects.filter (owner=user)
    qs = qs.exclude (status = Task.DONE)
    return qs.order_by ('priority')


@register.assignment_tag
def erp_get_tasks_by_username (username):
    qs = Task.objects.filter (owner__username=username)
    qs = qs.exclude (status = Task.DONE)
    return qs.order_by ('priority')


@register.assignment_tag
def erp_get_reminders (user=None):
    qs = Reminder.objects.filter (owner=user, date__gte=datetime.date.today())
    return qs.order_by ('date')


@register.assignment_tag
def erp_get_notes (user=None):
    return Note.objects.filter (owner=user)
