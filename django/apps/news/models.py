from django.db import models
from django.core.urlresolvers import reverse

import datetime

"""
TODO:
date => datetime
filter body for extra <p>'s at the end (old, imported articles)
some fields allows NULL since old data did that. fix db
publised field? (false for news tips)
db_index=True on Article.title?
if no body, redirect instead of showing on webpage?
"""

class Article (models.Model):
    ''' Link to external news article, with an optional own comment '''
    class Meta:
        #verbose_name = 'news link'
        verbose_name = 'nyhets-lenke'
        verbose_name_plural = 'nyhets-lenker'
        get_latest_by = 'date'

    pubdate =   models.DateField (auto_now_add=True)
    date =      models.DateField (default=datetime.datetime.now, help_text='Date of news article (url), not the day we posted it.')
    url =       models.URLField (unique=True, null=True) # @note some old news links have url=''
    title =     models.CharField (max_length=128)
    summary =   models.TextField (help_text=u'Just copy the "ingress" into this field.')
    body =      models.TextField (blank=True, null=True, help_text='Our comment to this news story. Usually empty.')

    def __unicode__ (self):
        return self.title

    def get_absolute_url (self):
        return reverse ('news-detail', args=[self.pk])
