from django.db import models
import datetime

"""
TODO:
filter body for extra <p>'s at the end (old, imported articles)
some fields allows NULL since old data did that. fix db
"""

class Article (models.Model):
    ''' Link to external news article, with an optional own comment '''
    class Meta:
        #verbose_name = 'news link'
        verbose_name = 'nyhets-lenke'
        verbose_name_plural = 'nyhets-lenker'
        get_latest_by = 'date'

    # @todo date & time?
    pubdate =   models.DateField (auto_now_add=True)
    date =      models.DateField (default=datetime.datetime.now, help_text='Date of news article (url), not the day we posted it.')
    # xxx default is wrong?
    url =       models.URLField (unique=True, null=True) # @note some old news links have url=''
    title =     models.CharField (max_length=128)
    summary =   models.TextField (help_text=u'Just copy the "ingress" into this field.')
    body =      models.TextField (blank=True, null=True, help_text='Our comment to this news story. Usually empty.')
    #body =      HtmlField (blank=True, null=True, help_text='Our comment to this news story. Usually empty.')

    def __unicode__ (self):
        return self.title

    @models.permalink
    def get_absolute_url (self):
        return ('news-detail', [str(self.pk)])
        # @todo just call reverse() instead?
        # if no body, return url instead? make our view redirect?
