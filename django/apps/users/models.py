from django.db import models
from django.contrib.auth.models import User


class Profile (models.Model):
    """ Profile attached to an user """
    user = models.OneToOneField (User)
    avatar =    models.ImageField (upload_to = 'avatar', blank=True)
    country =   models.CharField (max_length=30, blank=True)
#    about_me =  models.TextField (blank=True)

#    @models.permalink
#    def get_absolute_url (self):
#        return ('view_profile', None, {'username': self.user.username})

    def __unicode__ (self):
        s = self.user.get_full_name()
        if not s: s = self.user.username
        return s


## Create profile when new User object is created
from django.db.models.signals import post_save

def user_post_save (sender, instance, created, **kwargs):
    if created:
        Profile.objects.create (user=instance)

# @todo use lambda?
post_save.connect (user_post_save, sender=User)
#post_save.connect(create_profile, sender=User)
