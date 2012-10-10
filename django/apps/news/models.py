# App: News

from django.db import models


class Article (models.Model):
    ''' This is a help string. It's added to django.db.models.base.Model help str '''
    pub_date = models.DateField ('date published', auto_now_add=True)
      # @todo rename 'date'. should be date of news article
    url = models.URLField ()
    title = models.CharField (max_length=100)
    summary = models.TextField (max_length=1024)
    body = models.TextField ()
    # Default for fields: null=False, blank=False
    # NOTE: so fields are required (in admin, modelform, etc.). but
    # they (charfields) are not required when using DB api.
    # A: validation is not run by default when doing save :)
    #    so do a: o.full_clean(). it will throw ValidationError

    def __unicode__ (self):
        return self.title


# @todo rename Link?
# @note db table name is: news_articlelink  (so use underscore in name?)
class ArticleLink (models.Model):
    news        = models.ForeignKey (Article)
    url         = models.URLField ()
    title       = models.CharField (max_length=100)
    type        = models.IntegerField (choices = ((0, 'Les mer'),
                                                  (1, 'Video'),
                                                  (2, 'Bilder',)))

    def __unicode__ (self):
        return self.url
    # @todo link_type?
