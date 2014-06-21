from django.db import models

class Content (models.Model):
    ''' Content block used by various views/templates '''
    name = models.CharField (max_length=64, unique=True)
    content = models.TextField (blank=True)
    def __unicode__ (self): return self.name
