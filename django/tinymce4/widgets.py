from django import forms
#from django.utils.safestring import mark_safe


class TinyMCE (forms.Textarea):
    class Media:
        js = (
            '//tinymce.cachefly.net/4.1/tinymce.min.js',
            'js/core.js', 'tinymce4/tinymce.js',
        )

    def render (self, name, value, attrs=None):
        attrs['class'] = 'tinymce'
        return super(TinyMCE,self).render (name, value, attrs)
        # + mark_safe (u'some extra html')
