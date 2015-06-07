# coding: utf-8
from django.db import models

# TODO:
# cache controll: no-cache, etags, other?
# Date -> DateTime?
# optional: born_year?
# unique on name+city ?
class Petition (models.Model):
    CHOICES = (
        ('a', u'a) Nedkriminalisere cannabis (f.eks. etter Portugal-modellen).'),
        ('b', u'b) Avkriminalisere cannabis for de over 18 år.'),
        ('c', u'c) Avkriminalisere cannabis for de over 20 år.'),
        ('d', u'd) Regulere cannabis. Staten tar seg av produksjon og distribusjon.'),
    )
    date =   models.DateField (auto_now_add=True)
    # choice: form_class, choices_form_class. if these arguments are not
    # provided, CharField or TypedChoiceField will be used.
    choice = models.CharField (u'Jeg ønsker å', max_length=1, choices=CHOICES)
    name =   models.CharField (u'Navn', max_length=64)
    city =   models.CharField (u'Sted', max_length=64)
    public = models.BooleanField (u'Vis mitt navn i listen under', default=True)
    # @todo only add label to public view?

    def __unicode__ (self):
        return u'%c: %s, %s' % (self.choice, self.name, self.city)

    class Meta:
        verbose_name = 'opprop'
        verbose_name_plural = 'opprop'
        ordering = '-date',
        get_latest_by = 'date'
