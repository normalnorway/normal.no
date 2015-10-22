from django.db import models


class Category (models.Model):
    '''Link category'''
    name =  models.CharField (max_length=100)
    #comment = model.TextField (help_text='For internal use. Not shown on webpage.')

    def __unicode__ (self):
        return self.name

    class Meta:
        ordering = ['name']
        #verbose_name_plural = 'categories'
        verbose_name = 'kategori'
        verbose_name_plural = 'kategorier'


class Link (models.Model):
    '''Link to external site (Nettguide)'''
    category = models.ForeignKey (Category)
    name =     models.CharField (max_length=255)
    url =      models.URLField()
    text =     models.TextField ('description', blank=True)
    lang =     models.CharField ('Language', max_length=2, blank=True, help_text='Use a two character language code to show a flag beside the entry.')
    comment =  models.TextField (blank=True, help_text='For internal use. Not shown on webpage.')

    def __unicode__ (self):
        return self.name

    class Meta:
        verbose_name = 'lenke'
        verbose_name_plural = 'lenker'
