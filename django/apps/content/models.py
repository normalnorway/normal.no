# DEPRECATED - but can not remove before migrated to cms.Content

from django.db import models
from tinymce4.models import HtmlField

class Content (models.Model):
    '''Content block used by various views/templates'''

    name = models.CharField (max_length=64, unique=True)
    content = HtmlField (blank=True)

    class Meta:
        app_label = 'content' # why needed? RemovedInDjango19Warning
        verbose_name = 'innholds-blokk'
        verbose_name_plural = 'innholds-blokker'

    def __unicode__ (self):
        return self.name
