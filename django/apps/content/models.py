from django.db import models
from tinymce4.models import HtmlField

# class Page
# class Block
# user.has_perm ('content.change_page')
# user.has_perm ('content.change_block')

#class Page (models.Model):
#    class Meta:
#        permissions = (
#            ('can_change_gsf', 'Can change GSF-pages')
#        )


class Content (models.Model):
    '''Content block used by various views/templates'''

    name = models.CharField (max_length=64, unique=True)
    content = HtmlField (blank=True)

    class Meta:
        verbose_name = 'innholds-blokk'
        verbose_name_plural = 'innholds-blokker'

    def __unicode__ (self):
        return self.name
