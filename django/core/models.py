# Note: Not in use (yet)

from django.db import models
#from forms import TrimmedCharField # name conflict. rename TrimmedCharFormField?
import forms


# Note: This will only trim the data if it comes in through a form.
# @todo trim at the model layer?
class TrimmedCharField (models.CharField):
    """Like models.CharField but uses forms.TrimmedCharField"""
    __metaclass__ = models.SubfieldBase     # needed?
 
    description = 'Like CharField, but uses forms.TrimmedCharField'

    def formfield (self, **kwargs):
        #return super (TrimmedCharField, self).formfield (form_class=forms.TrimmedCharFormField, **kwargs)
        # more readable version of the line above
        kwargs['form_class'] = forms.TrimmedCharField
        return super (TrimmedCharField, self).formfield (**kwargs)


# Trim whitespace when saving models that do not have a form.
# Models without forms aren't validated by default.
# Shamelessly stolen from: http://stackoverflow.com/a/21265675
# @todo better name StripWhitespaceModelMixin? TrimFieldsMixin?
class ValidateModelMixin (object):
    """Mixin to strip whitespace from model fields"""

    def clean (self):
        for field in self._meta.fields: # @todo django 1.8 compatible?
            value = getattr (self, field.name)
            if not value: continue
            try: # ducktyping attempt to strip whitespace
                setattr (self, field.name, value.strip())
            except Exception:
                pass

    def save (self, *args, **kwargs):
        self.full_clean() # XXX this is not django's default behaviour!
        super (ValidateModelMixin, self).save (*args, **kwargs)
