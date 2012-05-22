from django.db import models

# @note name field defaults to mandatory.
# @todo if name not given, use filename

class File (models.Model):
    name = models.CharField(max_length=64)
    file = models.FileField(upload_to='media/files')
    # XXX uses filename as name. howto use pk?
    # upload/media/files/out.png
    # upload_to='/%Y/%m/%d' # supports strftime

    def __unicode__ (self):
        return self.name
