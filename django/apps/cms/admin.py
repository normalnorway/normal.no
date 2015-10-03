from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf.urls import url
from django.contrib import admin
from .models import Page, Content, File
from .forms import PageForm

admin.site.register (Content)


@admin.register (Page)
class PageAdmin (admin.ModelAdmin):
    fields = 'title', 'url', 'content', 'published', 'summary', 'image',
    list_display = 'url', 'title', 'modified', 'published',
    ordering = 'url',
    search_fields = 'url', 'title', 'content'
    list_filter = 'published',
    date_hierarchy = 'modified'
    form = PageForm
    #save_on_top = True # looks ugly

    def get_readonly_fields (self, request, obj=None):
        '''Make url read-only for existing pages'''
        if request.user.is_superuser: return []
        return [] if obj is None else ['url']

    def get_form (self, request, obj=None, **kwargs):
        '''Add request.user to the form so it can be used for validation'''
        form_class = super (PageAdmin, self).get_form (request, obj, **kwargs)
        if obj: return form_class
        # note: form_class and self.form is not the same
        # a: think it's because django modifies it. @see form_class.__mro__
        cls = type (form_class.__name__, (form_class,), dict(_user=request.user))
        return cls
        #return type ('SomeName', (form_class,), {'_user': request.user})
        # @todo add this (shorter) solution as comment here:
        # http://stackoverflow.com/a/9191583

    # note: save_form is *not* documented, so might be unsafe api
#    def save_form (self, request, form, change):
#        from django.forms import ValidationError
#        raise ValidationError ('dette gikk ikke')



@admin.register (File)
class FileAdmin (admin.ModelAdmin):
    ordering = 'name',
    readonly_fields = 'size', 'mimetype',
    #readonly_fields = '_size', 'mimetype',
    list_display = 'name', 'file', 'mimetype', '_size',
    list_filter = 'mimetype',
    actions = 'action_download',

    def _size (self, obj):
        from django.template.defaultfilters import filesizeformat
        return filesizeformat (obj.size)
    _size.admin_order_field = 'size'

    # @todo filter on file size? <10k, <100k, <1M, <10M, >10M

    def get_urls (self):
        wrap = self.admin_site.admin_view
        return [
            url (r'^upload_multiple/$', wrap (self.upload_multiple_view), name='file-upload-multiple'),
        ] + super (FileAdmin, self).get_urls()


    def upload_multiple_view (self, request):
        # Can not use bulk create since Model.save() won't be called.
        #File.objects.bulk_create (File(file=f) for f in request.FILES.getlist ('cmsfiles'))

        files = request.FILES.getlist ('cmsfiles')
        for uploaded_file in files:
            File.objects.create (file=uploaded_file)

        self.message_user (request, 'Uploaded %d files' % len(files))
        return redirect ('admin:cms_file_changelist')


    # Note: Creates zipfile in memory
    # Note: WinZip interprets all file names as CP437, also known as DOS Latin.
    # Note: Default is ZIP_STORED
    # Update: Django 1.8 has FileResponse for streaming binary files
    def action_download (self, request, queryset):
        if len (queryset) == 1:
            obj = queryset[0]
            assert obj.mimetype
            response = HttpResponse (obj.file, content_type=obj.mimetype) # @todo use streaming response?
            response['Content-Disposition'] = 'attachment; filename="%s"' % obj.file.name.split('/')[-1]
            # response['Content-Length'] = <filesize>
            # response['X-Sendfile'] = '/path/to/secret/file'
            return response

        # Multiple files selected, so return a zipfile
        from os.path import basename
        #from zipfile import ZipFile
        import zipfile
        from io import BytesIO
        from uuid import uuid4
        outbuf = BytesIO()
        with zipfile.ZipFile (outbuf, 'w') as zfile:
            for obj in queryset:
                ctype = zipfile.ZIP_DEFLATED
                if obj.mimetype.startswith ('image/'):
                    ctype = zipfile.ZIP_STORED
                if obj.mimetype.startswith ('application/'):
                    ctype = zipfile.ZIP_STORED
                zfile.write (obj.file.path, basename (obj.file.path), ctype)
        outbuf.seek (0)
        filename = uuid4().hex + '.zip'
        response = HttpResponse (outbuf, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
    action_download.short_description = 'Download selected files'
