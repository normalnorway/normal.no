# encoding: utf-8
from datetime import datetime
from django.contrib.syndication.views import Feed
#from django.core.urlresolvers import reverse
#from django.utils import timezone
from . models import Article

# @todo cache?
# @todo enable ttl?

# Better description?
#   I nyhetsarktivet finner du lenker til de fleste cannabis-relaterte saker
#   omtalt i norsk media. I tillegg til en del utenlandske saker.
#   Arkiv: http://normal.no/nyheter/arkiv/

class NewsFeed (Feed):
    title = 'Normals nyhetsarkiv'
    description = u'Cannabisrelaterte nyheter i norske medier. Arkiv: http://normal.no/nyheter/arkiv/'
    categories = ('cannabis', 'hasj', 'marihuana', 'rus', 'ruspolitikk', 'nyheter')
    link = '/nyheter/rss/'

    # These have no effect :(
    #author_name = u'Normal – Norsk organisasjon for reform av marihuanalovgivningen'
    #author_email = 'post@normal.no'
    #author_link = 'http://normal.no/om'
    #feed_copyright = 'No Copyright (c) 2015, Normal'
    # But author_* is supported per article by using item_author_*()

    # Not included if not set
    #ttl = 3600


    def items (self):
        """ Articles to include in the feed """
        return Article.pub_objects.order_by ('-date')[:25]


    ## Handle item fields: item_<field>

    def item_link (self, item):
        return item.url if item.url else item.get_absolute_url()
        #return item.url if item.url else reverse ('news-detail', args=[item.id])
        # Articles without url  => link to own view
        # Articles with url     => link directly to external news story (url)

    def item_pubdate (self, item):
        """ Note: will set Last-Modified header based on this """
        return datetime.combine (item.date, datetime.min.time())
        # @todo use real time, not fake it

    def item_description (self, item):
        return item.summary

    # Note: Need this. Without the string is not marked as safe,
    # and there will be troubles with quotes, etc.
    def item_title (self, item):
        return item.title

    # @todo enable and return true for articles that have canonical url
    #def item_guid_is_permalink (self, obj):
    #    return obj.permalink != ''
