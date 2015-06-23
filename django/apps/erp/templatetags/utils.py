import datetime, calendar

def _flatten (lst): return sum (lst, [])

# @todo has_key -> in

class MyCalendar (calendar.HTMLCalendar):
    def __init__ (self, marks=None):
        super (MyCalendar, self).__init__ (0)
        self.marks = marks

    def formatmonth (self, theyear, themonth, withyear=True):
        self._marks = self.marks.get_month_marks (theyear, themonth)
        return super (MyCalendar, self).formatmonth (theyear, themonth, withyear)

    def formatday (self, day, weekday):
        if day == 0: return '<td class="noday">&nbsp;</td>' # day outside month
        if day not in self._marks:
            return '<td class="%s">%d</td>' % (self.cssclasses[weekday], day)
        mlst = self._marks[day]
        csscls = _flatten ([obj.csscls for obj in mlst])
        csscls.append (self.cssclasses[weekday])
        csscls.append ('marked')
        #title = '\n'.join (obj.title for obj in mlst)
        title = '- ' + '\n- '.join (obj.title for obj in mlst)
        return '<td class="%s"><a href="%s" title="%s">%d</a></td>' % \
               (' '.join(csscls), '#', title, day)

#        if mark.url:
#            return '<td class="%s"><a href="%s" %s>%d</a></td>' % (','.join(csscls), mark.url, title, day)
#        if not mark.url:
#            return '<td class="%s" %s><strong>%d</strong></a></td>' % \
#                    (','.join (csscls), title, day)
 



class _DateMarker (object): # MarkedDate
    title = None
    url = None
    csscls = []
    def __init__ (self, title='', url=None, csscls=None):
        self.title = title
        if url: self.url = url
        if csscls: self.csscls = csscls
    def __repr__ (self):
        return u'<DateMarker: %s>' % self.title


from collections import defaultdict

# @todo merge with MyCalendar? MarkDateMixin?
class DateMarks (object):
    def _mk_year_list (self):
        '''list of months. month entry is dict (key=day, val=[])'''
        return [defaultdict (list) for nil in range(13)]

    def __init__ (self):
        self.years = defaultdict (self._mk_year_list) # mk_month_list

    def add (self, date, title='', url=None, csscls=None):
        obj = _DateMarker (title, url, csscls)
        mlist = self.years[date.year]
        mlist[date.month][date.day].append (obj)

    def get_month_marks (self, year, month):
        '''Returns dict where days are keys'''
        if not self.years.has_key (year): return {}
        #return self.years[year][month] # faster
        return dict(self.years[year][month])


if __name__ == '__main__':
    today = datetime.date.today()
    marks = DateMarks()
    marks.add (today, 'Today!', csscls=['today'])
    marks.add (datetime.date (2015,6,29), title='Do stuff', csscls=['meeting'])
    marks.add (datetime.date (2015,6,29), title='Pule', url='sex.com', csscls=['red', 'blue'])
    marks.add (datetime.date (2015,7,5), title='Grille')

    from pprint import pprint
#    pprint (marks.years[2015])
#    pprint (marks.get_month_marks (2015, 6))

    def _flatten (lst): return sum (lst, [])

    mlst = marks.get_month_marks (2015, 6)[29]
    print ' '.join (_flatten ([obj.csscls for obj in mlst]))


    #cal = MyCalendar (dates=dates)
    #print cal.formatmonth (2015, 6)
