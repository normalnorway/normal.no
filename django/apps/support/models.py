# -*- encoding: utf-8 -*-

from django.db import models


# @todo unique on name+city
# @todo born_year?
class Petition (models.Model):
    CHOICES = (
#        (None, None),
        (1, u'1) Nedkriminalisere cannabis (f.eks. etter Portugal-modellen).'),
        (2, u'2) Avkriminalisere cannabis for de over 18 år.'),
        (3, u'3) Avkriminalisere cannabis for de over 20 år.'),
        (4, u'4) Regulere cannabis. Staten tar seg av produksjon og distribusjon.'),
    )
    date =   models.DateField (auto_now_add=True)
    #choice = models.PositiveSmallIntegerField (u'Jeg ønsker å', choices=CHOICES, blank=True) # trying to get rid of "-------"
    choice = models.PositiveSmallIntegerField (u'Jeg ønsker å', choices=CHOICES)
    name =   models.CharField (u'Navn', max_length=64)
    city =   models.CharField (u'Sted', max_length=64)
    public = models.BooleanField (u'Vis mitt navn i listen under', default=True)
