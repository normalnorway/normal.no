from django.db import models
import datetime
#from tinymce4.models import HtmlField

"""
TODO:
utenriks-field (or use tags for that. or domain)
tags field
filter body for extra <p>'s at the end (old, imported articles)
"""

class Article (models.Model):
    ''' Link to external news article, with an optional own comment '''
    # Note: some fields allows NULL since old data did that. @todo fix db
    class Meta:
        #verbose_name = 'News link'
        verbose_name = 'Nyhets-lenke'
        verbose_name_plural = 'Nyhets-lenker'
        get_latest_by = 'date'

    pubdate =   models.DateField (auto_now_add=True)
    date =      models.DateField (default=datetime.datetime.now, help_text='Date of news article (url), not the day we posted it.')
    url =       models.URLField (unique=True, null=True) # @note some old news links have url=''
    title =     models.CharField (max_length=128)
    summary =   models.TextField (help_text=u'Just copy the "ingress" into this field.')
    body =      models.TextField (blank=True, null=True, help_text='Our comment to this news story. Usually empty.')
    #body =      HtmlField (blank=True, null=True, help_text='Our comment to this news story. Usually empty.')

    def __unicode__ (self): return self.title

    @models.permalink
    def get_absolute_url (self):
        return ('news-detail', [str(self.pk)])
