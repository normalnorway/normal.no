'''
Import old "nettguide".
'''

import sys
import re
from lxml import etree

# Let 'print' handle unicode when piping or redirecting
import codecs
if not sys.stdout.isatty():
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)


''' ----------------------- '''
''' EXPORT FROM OLD WEBSITE '''
''' ----------------------- '''

# HTMLParser (remove_blank_text=True, encoding='latin1', remove_comments=True, remove_pis=True)
tree = etree.parse (sys.argv[1], etree.HTMLParser(remove_comments=True))
html = tree.getroot()

nettguide = []

dlindex = 0
dllist = html.xpath('//div[@id="content"]/*')
while dlindex+1 < len(dllist):          ## For each section
    h3 = dllist[dlindex]
    dl = dllist[dlindex+1]
    dlindex += 2

#    print '=== %s ===\n\n' % h3.text
    section = []
    nettguide.append ((h3.text, section))

    index = 0
    nodelist = list(dl.iterchildren())
    while index+1 < len(nodelist):      ## For each entry
        entry = {}
        dt = nodelist[index]

        l = dt.xpath ('img/@src')
        if l:
            m = re.match ('pics/([a-z]{2})1.gif', l[0])
            entry['lang'] = m.group(1)
        else:
            entry['lang'] = ''

        if nodelist[index+1].tag == 'dd':    # dd tag is optional
            dd = nodelist[index+1]
            index += 2
        else:
            dd = None
            index += 1

        a = dt.xpath('a|A')[0]
        entry['url']   = a.get('href')
        entry['name'] = ''.join(list(a.itertext())).strip()

#        print 'Title:\t', entry['title']
#        print 'URL:\t', entry['url']

        if dd != None:
            s = etree.tostring(dd, encoding=unicode)
            s = s[4:-5]     # remove surrounding <dd> tag
            s = s.replace ('\r', '')    # use regex instead?
            entry['text'] = s.replace('\n', ' ').strip()
        else:
            entry['text'] = ''

#        print 'DD:\t', entry['text']
        section.append (entry)


#from pprint import pprint
#pprint(nettguide)



''' ----------------------- '''
'''         IMPORT          '''
''' ----------------------- '''

import initdjango
from apps.links.models import Category as LinkCategory
from apps.links.models import Link

LinkCategory.objects.all().delete()
Link.objects.all().delete()

# Q: why slow?  A: wrap in transaction
# @todo obj.full_clean()?
for (section, data) in nettguide:
    print 'Importing ' + section
    category = LinkCategory.objects.create (name=section)
    for entry in data:
        entry['category'] = category
        Link.objects.create (**entry)
