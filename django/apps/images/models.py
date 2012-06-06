from django.db import models

# @todo inherit from apps.files? ImageField inherits from FileField
class Image (models.Model):
    name =   models.CharField (max_length = 64, blank=True)
    file =   models.ImageField (upload_to = 'images',
                                width_field = 'width',
                                height_field = 'height')
    width  = models.PositiveSmallIntegerField (editable=False)
    height = models.PositiveSmallIntegerField (editable=False)
    # error_message = { "invalid": 'error message when fails' }

    def __unicode__ (self):
        return self.name


# Used by Dojo.editor
class EditorImage (models.Model):
    file = models.ImageField (upload_to = 'editor')
