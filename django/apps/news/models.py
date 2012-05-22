# App: News

from django.db import models


class Article (models.Model):
    pub_date = models.DateField ('date published')
    url = models.URLField ()
    title = models.CharField (max_length=100)
    summary = models.TextField (max_length=1024)
    body = models.TextField ()

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
