'''
Export articles from the old website, and import them into
new Django based website.

@todo rename importnews.py?
@bug pubdate not set (since editable=False)
@bug when using sqlite, must be run in same directory as db file
@bug 1285650416 # feed://www
'''


import sys
import os
import codecs
import locale
import re
from datetime import datetime
from StringIO import StringIO

import initdjango
from apps.news.models import Article as NewsArticle

from django.conf import settings
settings.DEBUG = False


class Exporter:
    """
    Export one news article from the old system, return it as a dict.
    """
    def __init__(self, filename):
        #self.file = codecs.open (filename, encoding='latin1')
        self.file = codecs.open (filename, encoding='windows-1252')
        self.data = None
        self.re1 = re.compile ('^\n')
        self.re2 = re.compile (r'<a noauto')
        self.re3 = re.compile (r'\b(http://[^\s]+)(\s)', re.I)
        self.re4 = re.compile (r'\b(www(\.\w+)+)\b', re.I)
        self.re5 = re.compile (r'\b([\w\.-]+\@\w+(\.\w+)+)\b', re.I)
        self.reurl = re.compile (r'"(http://[^"]+)">.*?</a>', re.I)
        # @todo make regex class static

    def get (self):
        if not self.data:
            self.data = self.parse_header()
            self.data['body'] = self.parse_body()
        return self.data

    # TODO: better way. don't emulate old behavior
    # - Nuke blank lines at the end.
    # - Nuke multiple blank lines
    # - Respect line breaks (unless line already ends with '<br>'. @see 0980819647
    # - Blank line separates paragraphs (and use </p> tag? valid html without?)

    # Do same magic on 'body' as old 'viewnews' script.
    # @note link transform on body is done per line
    # MAGIC:
    # 1) /^n/ -> '<p>'
    # 2) /<a noauto/ -> print line, then contine
    # 3) convert 'http://*' to link
    # 4) if not http:// link, convert 'www.*' to link
    # 5) convert '*@*' to mailto-link
    #
    # Old script did not do this!
    # @todo html encode? A: if line contains no link/transform or html code, then can & -> &amp;
    # @todo if (m|http://|) { s/&/&amp;/g; }  # only when showing url on frontpage (makenews)
    # @todo If body only contains one link and up to 25 char of extra text,
    #       then nuke body.
    def parse_body (self):
        buf = StringIO()
        for line in self.file:
            if self.re1.search (line):
                buf.write ('\n<p>')
            line = line.strip(" ")
            if self.re2.search (line):
                buf.write (line)
                continue
            (s,n) = self.re3.subn (r'<a href="\1">\1</a>\2', line)
            if n:
                line = s
            else:
                line = self.re4.sub (r'<a href="http://\1">\1</a>', line)
            line = self.re5.sub (r'<a href="mailto:\1">\1</a>', line)
            buf.write (line)

        #body = buf.getvalue().strip()
        body = buf.getvalue()
        buf.close()

        # extract and set self.data['url']
        m = self.reurl.search (body)
        if m:
            self.data['url'] = url = m.group(1)
            # drop body if only one url and rest is less than 25 chars
            if not self.reurl.search (body, m.end()) and len(body)-m.end() < 25:
                body = None
        else:
            self.data['url'] = ''

        return body


    ''' Parse headers. I.e., everything but the body '''
    def parse_header (self):
        f = self.file

        ts = int(os.path.basename(f.name))
        pubdate = datetime.fromtimestamp(ts).date()

        title = f.readline().strip()

        date = datetime.strptime (f.readline().strip(), '%d. %B %Y').date()
        assert pubdate >= date

        assert f.readline() == '\n'

        #summary = f.readline().strip()
        #assert f.readline() == '\n'

        # @todo try to add '.' if last line ends with \w?
        summary = ''
        while True:
            s = f.readline()
            if s == '\n':
                break
            summary += s
        summary = summary.strip()

        # now only the body is left to parse

        return dict(pubdate=pubdate, date=date, title=title, summary=summary)




    ### MAIN ###
if __name__ == '__main__':

    if (len(sys.argv) != 2):
        die ('Usage: %s <filename>' % sys.argv[0])

    locale.setlocale(locale.LC_TIME, 'nb_NO')   # parsing norwegian dates

    pathname = sys.argv[1]

    # Debug mode: Dump one article to stdout
    if os.path.isfile(pathname):
        data = Exporter(pathname).get()
        #print data
        print data['body']
        #print data['url']
        sys.exit(0)

#    NewsArticle.objects.all().delete()
#    sys.exit(0)
#    print len(os.listdir (pathname))
#    sys.exit(0)

    # Import all articles in directory
    instances = []
    refile = re.compile ('\d+$')
    for filename in os.listdir (pathname):
        path = os.path.join (pathname, filename)
        if re.match ('\d+$', filename):
            print 'Exporting ' + filename
            instances.append ((filename, NewsArticle(**Exporter(path).get())))
            #instances.append (NewsArticle(**Exporter(path).get()))

#            if len(instances) > 100:
#                print 'Importing %d articles ...' % len(instances)
#                NewsArticle.objects.bulk_create (instances)
#                instances = []

            #print 'Importing ' + filename
            #NewsArticle.objects.create (**Exporter(path).get())
            #o = NewsArticle (**Exporter(path).get())
            #o.save()
            #o.save (force_insert=True)
            #o.full_clean()	# do model validation
        else:
            print 'Skipping ' + filename

#    print 'Importing %d articles ...' % len(instances)
#    NewsArticle.objects.bulk_create (instances)
    for (f,o) in instances:
        #print 'Importing: %s' % o.title
        print 'Importing: %s' % f
        if o.summary == '':
            print 'XXX'
            continue
        #o.full_clean()
        o.save(force_insert=True)
