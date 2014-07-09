from django.db import models
import datetime

"""
TODO:
utenriks-field (or use tags for that. or domain)
extra fields: user, tags, published?
filter body for extra <p>'s at the end (old, imported articles)
"""

class Article (models.Model):
    ''' Link to external news article, with an optional own comment '''
    class Meta:
        verbose_name = 'News link'
        get_latest_by = 'date'

    pubdate =   models.DateField (auto_now_add=True)
    date =      models.DateField (default=lambda: datetime.datetime.now(), help_text='Date of news article (url), not the day we posted it.')
    url =       models.URLField ('Link', unique=True, null=True) # @note some old news links have url=''
                # @note underlaying db coloumn allows NULL since old articles might contain a blank url
    title =     models.CharField (max_length=128)
    summary =   models.TextField (help_text=u'Just copy the "ingress" into this field.')
    body =      models.TextField (blank=True, null=True, help_text='Our comment to this news story')
    # Q: why null=True on body?

    def __unicode__ (self): return self.title

    @models.permalink
    def get_absolute_url (self):
        return ('news-detail', [str(self.pk)])
