from django.db import models
import datetime

# @todo utenriks-field (or use tags for that)
# @todo owner-field
# @todo tags
# @todo clean() method that strip() string fields?
class Article (models.Model):
    '''
    Link to an external news article, with an optional own comment.
    '''
    pubdate = models.DateField (editable=False, auto_now_add=True, verbose_name='Date published')
    date = models.DateField (default=datetime.datetime.now(), help_text='Date of news article (url), not the day we posted it.')
    url = models.URLField (blank=True)
    title = models.CharField (max_length=255)
    summary = models.TextField()	# abstract?
    body = models.TextField (blank=True, null=True, help_text='Own text, like our comment.')

    def __unicode__ (self):
        return self.title


'''
class ArticleLink (models.Model):
    news        = models.ForeignKey (Article)
    url         = models.URLField ()
    title       = models.CharField (max_length=100)
    type        = models.IntegerField (choices = ((0, 'Les mer'),
                                                  (1, 'Video'),
                                                  (2, 'Bilder',)))
    def __unicode__ (self):
        return self.type + self.url
'''
