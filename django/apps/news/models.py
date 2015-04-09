from django.db import models
from django.core.urlresolvers import reverse

"""
TODO:
filter body for extra <p>'s at the end (old, imported articles)

DB-changes:
- db_index=True on published!!
- rename Article -> NewsLink
- bool field: user_submitted?
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

    # Note: date, title, and summary are required fields when adding
    # trough the admin. News tips are incomplete objects and the only
    # required field is url; these have published forced to False.

    # Note: 'date' can have empty time (00:00).
    #       @todo module method to format as string

    # Managers
    # Note: The first manager is the default; don't change that!
    objects = models.Manager()
    pub_objects = PubArticleManager()   # publicly available objects

    # Fields
    pubdate =   models.DateTimeField (auto_now_add=True)
    url =       models.URLField (unique=True, null=True) # Note: some old news links don't have url set, therefore must allow null (since unique=True)
    date =      models.DateTimeField (null=True, help_text='Date of news article (url), not the day we posted it.')
    title =     models.CharField (max_length=128)
    summary =   models.TextField (help_text=u'Just copy the "ingress" into this field.')
    body =      models.TextField (blank=True, help_text='Our comment to this news story. Usually empty.')
    image_url = models.URLField (blank=True)
    published = models.BooleanField (default=True)
    url_is_canonical = models.BooleanField ('Is canonical?', default=False)
      # @todo better to store both urls?
      # note: is_canonical=False really means we don't know, so it's
      #       better to use NullBooleanField or choices=('Y', 'N', 'U')
      # note: label is for admin (Is url canonical? is more general)

    def get_date (self):
        """Time might be empty, handle that by returning datetime.time"""
        import datetime
        t0 = datetime.time()
        if self.date.time() == t0: return self.date.date()
        return self.date
        # @todo "5. mars 2015 22:51" => "5. mars 2015, kl. 22:51"

    def __unicode__ (self):
        return self.title

    def get_absolute_url (self):
        return reverse ('news-detail', args=[self.pk])
