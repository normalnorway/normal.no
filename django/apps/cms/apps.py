from django.apps import AppConfig
from django.db.models.signals import post_delete


def cb_post_delete_file (sender, **kwargs):
    kwargs['instance'].file.delete (save=False) # delete underlying file


class CmsAppConfig (AppConfig):
    name = 'apps.cms'
    verbose_name = 'Content management'
    #label = 'CMS'

    def ready (self):
        #File = self.get_model ('File')
        post_delete.connect (cb_post_delete_file,
                             sender='cms.File',
                             dispatch_uid='c15be48320e')
