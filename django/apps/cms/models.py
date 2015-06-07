# coding: utf-8
from django.core.urlresolvers import reverse
from django.db import models
from tinymce4.models import HtmlField


class Page (models.Model):
    url = models.CharField (max_length=150, unique=True)
    title = models.CharField (max_length=75)    # blank=True?
    content = HtmlField()
    # published = models.BooleanField()
    # in_menu = models.BooleanField()   # menu_name: default to title
    # template = models.CharField (max_length=75)
    # extra_acl: to allow users to edit a subset of the pages
    # @todo allow blank/null urls, so can hardcode /foo url to Page.id
    # @todo make title default to url?
    # @todo use url as primary key? A: no

    def __unicode__ (self):
        return self.title

    def get_absolute_url (self):
        return reverse ('cms:page', args=[self.url])

#    class Meta:
#        permissions = (
#            ('change_page_gsf', u'Can change «gruppesøksmål»-pages'),
#        )


# class Block
# user.has_perm ('cms.change_page')
# user.has_perm ('cms.change_page_<extraacl>')  ??
# user.has_perm ('cms.change_block')
