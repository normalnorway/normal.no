import datetime
from django.db import models
from django.core.urlresolvers import reverse
#from django.conf.settings import AUTH_USER_MODEL
from django.conf import settings


_empty_time = datetime.time()


class PubArticleManager (models.Manager):
    """Only returns objects with published=True"""
    def get_queryset (self):
        qs = super(PubArticleManager,self).get_queryset()
        return qs.filter (published=True)


class Article (models.Model):   # NewsLink
    """Link to external news article, with an optional own comment

    Note: date, title, and summary are required fields when adding
    trough the admin. News tips are incomplete objects and the only
    required field is url; these have published forced to False.

    The date field can have empty time (00:00), so use get_date helper

    Some old objects have empty url, so must allow null (since unique=True).
    """
    class Meta:
        verbose_name = 'nyhets-lenke'
        verbose_name_plural = 'nyhets-lenker'
        get_latest_by = 'date'

    # Managers. The first manager is the default; don't change that!
    objects = models.Manager()
    pub_objects = PubArticleManager() # objects where published is True

    # Fields
    # @todo drop index on user field
    # CREATE INDEX "news_article_e8701ad4" ON "news_article" ("user_id");
    user =      models.ForeignKey (settings.AUTH_USER_MODEL, blank=True, null=True)
    pubdate =   models.DateTimeField (auto_now_add=True)
    url =       models.URLField (unique=True, null=True, max_length=255) # Note: MySQL does not allow unique CharFields to have a max_length > 255 :(
    date =      models.DateTimeField (null=True, db_index=True, help_text='Date of news article (url), not the day we posted it.')
    title =     models.CharField (max_length=128)
    summary =   models.TextField (help_text=u'Just copy the "ingress" into this field.')
    body =      models.TextField (blank=True, help_text='Our comment to this news story. Usually empty.')
    image_url = models.URLField (blank=True) # note: max_length=200
    published = models.BooleanField (default=True)
    url_is_canonical = models.BooleanField ('Is canonical?', default=False)
    # note: url_is_canonical=False really means we don't know, so it's
    #       better to use NullBooleanField or choices=('Y', 'N', 'U')

    def get_date (self):
        """Time might be empty. Returns datetime.date or datetime.datetime"""
        return self.date if self.date.time()!=_empty_time else self.date.date()

    def get_url (self):
        """If no own comment (body), then link directly to the external url"""
        return self.get_absolute_url() if self.body else self.url

    def __unicode__ (self):
        return self.title

    def get_absolute_url (self):
        return reverse ('news-detail', args=[self.pk])
