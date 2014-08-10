# -*- encoding: utf-8 -*-

from django.db import models


# @todo unique on name+city
# @todo born_year?
class Petition (models.Model):
    CHOICES = (
        ('a', u'a) Nedkriminalisere cannabis (f.eks. etter Portugal-modellen).'),
        ('b', u'b) Avkriminalisere cannabis for de over 18 år.'),
        ('c', u'c) Avkriminalisere cannabis for de over 20 år.'),
        ('d', u'd) Regulere cannabis. Staten tar seg av produksjon og distribusjon.'),
    )
    date =   models.DateField (auto_now_add=True)
    #choice = models.PositiveSmallIntegerField (u'Jeg ønsker å', choices=CHOICES, blank=True) # trying to get rid of "-------"
    choice = models.CharField (u'Jeg ønsker å', max_length=1, choices=CHOICES)
      # The form field class can be specified via the form_class and
      # choices_form_class arguments. If these arguments are not provided,
      # CharField or TypedChoiceField will be used.
    name =   models.CharField (u'Navn', max_length=64)
    city =   models.CharField (u'Sted', max_length=64)
    public = models.BooleanField (u'Vis mitt navn i listen under', default=True)
    #public = models.BooleanField (default=True)

    def __unicode__ (self):
        return u'%c: %s, %s' % (self.choice, self.name, self.city)
