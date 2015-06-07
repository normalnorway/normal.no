# Note: Not in use (yet)

print "forms.py"

from django import forms

# The clean method runs after any validation. So if you're doing some
# regex validation that doesn't allow leading / trailing spaces for
# instance, the validation will fail. It's better to trim the whitespace
# first, then do the validation.

class TrimmedCharField (forms.CharField):
    """Works like CharField but will trim whitespaces"""
    def clean (self, value):
        return value.strip ()
        # Q: can value be None?
        # Q: chain up?
        #return super (TrimmedCharField, self).clean (value)
# However, the best place to do this is in your view after the form has
# been validated; before you do any inserts into the db or other
# manipulation of data if you are using ModelForms.


# Shamelessly stolen from: http://stackoverflow.com/a/21265675
# This mixin can be used with both Form and ModelForm.
class StripWhitespaceMixin (object):
    """Mixin to strip whitespace from all form fields"""
    def _clean_fields (self):
        for name, field in self.fields.items ():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because
            # some widgets split data over several HTML fields.
            value = field.widget.value_from_datadict (self.data, self.files, self.add_prefix (name))
            try:
                if isinstance (field, forms.FileField):
                    initial = self.initial.get (name, field.initial)
                    value = field.clean (value, initial)
                else:
                    if isinstance (value, basestring): # strip strings
                        value = field.clean (value.strip())
                    else:
                        value = field.clean (value)
                self.cleaned_data[name] = value
                if hasattr (self, 'clean_%s' % name):
                    value = getattr (self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except forms.ValidationError as ex:
                self._errors[name] = self.error_class (ex.messages)
                if name in self.cleaned_data:
                    del self.cleaned_data[name]
