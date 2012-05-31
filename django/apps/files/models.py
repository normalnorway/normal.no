from django.db import models

# @note name field defaults to mandatory.
# @todo if name not given, use filename

# @todo in admin view, show "fake" fields (of FileField)
# f.size, f.name, f.path

class File (models.Model):
    name = models.CharField (max_length = 64)
    file = models.FileField (upload_to = 'media/files')
    # XXX uses filename as name. howto use pk?
    # update: but add numeric prefix if name clashes
    # upload/media/files/out.png
    # upload_to='/%Y/%m/%d' # supports strftime
    # @note admin interface do *not* delete the files (only db entries)

    def __unicode__ (self):
        return self.name
