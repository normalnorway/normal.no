from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse

"""
TODO:
filter body for extra <p>'s at the end (old, imported articles)
some fields allows NULL since old data did that. fix db
  update: can't, since field also is unique (that only works with null, since null!=null)
if no body, redirect instead of showing on webpage?

DB-changes:
- rename Article -> NewsLink
- image_url field
- add field for canonical_url (or url_original)?
- db_index=True on Article.title?
"""


class PubArticleManager (models.Manager):
    """Only returns objects with published=True"""
    def get_queryset (self):
        qs = super(PubArticleManager,self).get_queryset()
        return qs.filter (published=True)


class Article (models.Model):
    """Link to external news article, with an optional own comment"""
    class Meta:
        #verbose_name = 'news link'
        verbose_name = 'nyhets-lenke'
        verbose_name_plural = 'nyhets-lenker'
        get_latest_by = 'date'

    # Managers
    # Note: The first manager is the default; don't change that!
    objects = models.Manager()
    pub_objects = PubArticleManager()   # publicly available objects

    # Fields
    pubdate =   models.DateTimeField (auto_now_add=True)
    date =      models.DateTimeField (default=datetime.now, help_text='Date of news article (url), not the day we posted it.')
    url =       models.URLField (unique=True, null=True) # Note: some old news links don't have url set, therefore must allow null
    title =     models.CharField (max_length=128)
    summary =   models.TextField (help_text=u'Just copy the "ingress" into this field.')
    body =      models.TextField (blank=True, help_text='Our comment to this news story. Usually empty.')
    published = models.BooleanField (default=True) # help_text='Show on webpage?')
      # Note: this will *not* add a sql default, so published will only
      # default to True when created through Django. But sql will not
      # allow null so will get error if omitting published in sql.
      # Can manually edit the database to get around it ...
      # http://stackoverflow.com/questions/6153482/django-models-default-value-for-column

    def __unicode__ (self):
        return self.title

    def get_absolute_url (self):
        return reverse ('news-detail', args=[self.pk])
