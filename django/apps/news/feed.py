from datetime import datetime
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
#from django.utils import timezone
from . models import Article

# @todo cache?

class NewsFeed (Feed):
    title = 'Normals nyhetsarkiv'
    link = '/rss/'
    description = 'bla, bla, bla'
    author_name = 'Normal'
    author_email = 'post@normal.no'
    #ttl = 600

    def items (self):
        return Article.objects.order_by ('-date')[:25]

    def item_link (self, item):
        return item.url # link directly to external news story

    # Note: will set Last-Modified header based on this
    def item_pubdate (self, item):
        return datetime.combine (item.date, datetime.min.time())
        # @todo use real time, not fake it

    def item_description (self, item):
        return item.summary

    # title -> title
