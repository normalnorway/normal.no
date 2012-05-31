from django.db import models
from django.contrib.auth.models import User


class Profile (models.Model):
    # Link to User
    user = models.OneToOneField (User)

    # Extra profile fields
    country = models.CharField (max_length=30)
    bio = models.TextField()

    def __unicode__ (self):
        s = self.user.get_full_name()
        if not s: s = self.user.username
        return s


## Create profile when new User object is created
from django.db.models.signals import post_save

def create_profile (sender, instance, created, **kwargs):
    print "User: post_save"
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
