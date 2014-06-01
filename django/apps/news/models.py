from django.db import models
import datetime

# @todo utenriks-field (or use tags for that)
# @todo owner-field
# @todo clean() method that strip() string fields?
class Article (models.Model):
    '''
    Link to an external news article, with an optional own comment.
    '''
    pubdate = models.DateField (editable=False, auto_now_add=True, verbose_name='Date published')
    date = models.DateField (default=datetime.datetime.now(), help_text='Date of news article (url), not the day we posted it.')
    url = models.URLField (blank=True)  # @todo unique! and way to list duplicate titles
    title = models.CharField (max_length=255)   # @todo 100?
    summary = models.TextField()	# abstract?
    body = models.TextField (blank=True, null=True, help_text='Own text, like our comment.')

    def __unicode__ (self):
        return self.title

    @models.permalink
    def get_absolute_url (self):
        return ('news-detail', [str(self.pk)])



# @todo delete image file
# @todo need image_width to wrap image text
class Story (models.Model):
    ''' Short news story / "Aktuelt" '''
    class Meta:
        verbose_name_plural = 'stories'

    ALIGNMENT = (('l', 'Left'), ('r', 'Right'))

    date = models.DateField (default=datetime.datetime.now())
    published = models.BooleanField (default=True)
    title = models.CharField (max_length=100)
    abstract = models.TextField (blank=True)
    text = models.TextField (help_text='NOTE: Supports Markdown syntax. (<a href="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet" target="_blank">Se here for help.</a>)')
    image = models.ImageField (blank=True, upload_to='images/news_story')
    image_text = models.CharField (blank=True, max_length=255)
    image_align = models.CharField (max_length=1, choices=ALIGNMENT, default='r')
    comment = models.TextField (blank=True, help_text='Internal comment. Not shown on the website.')

    def __unicode__ (self):
        return self.title

    @models.permalink
    def get_absolute_url (self):
        return ('news-story-detail', [str(self.pk)])
