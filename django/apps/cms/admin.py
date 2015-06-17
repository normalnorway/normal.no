from django.http import HttpResponse
from django.contrib import admin
from .models import Page, Content, File

# can put save buttons on top?

admin.site.register (Content)


@admin.register (Page)
class PageAdmin (admin.ModelAdmin):
    ordering = 'url',
    list_display = 'url', 'title',
    search_fields = 'url', 'title', 'content'
    def get_readonly_fields (self, request, obj=None):
        return [] if obj is None else ['url']
    # @todo filter on startswith(/). filter on url depth



@admin.register (File)
class FileAdmin (admin.ModelAdmin):
    ordering = 'name',
    readonly_fields = 'size', 'mimetype',
    list_display = 'name', 'file', 'mimetype', 'size',
    list_filter = 'mimetype',
    actions = 'action_download',

    def get_urls (self):
        from django.conf.urls import url
        return [
            url (r'^upload/$', self.view_upload),
            #url (r'^(?P<member_id>\d+)/prev/$', self.prev_view),
            #url (r'^send-giro/$', self.admin_site.admin_view (self.send_giro_view)),
        ] + super (FileAdmin, self).get_urls()

    def view_upload (self, request):
        from django.shortcuts import render
        return render (request, 'file/upload.html', dict(foo=321))
        #return render (request, 'admin/cms/file/upload.html', dict(foo=321))
        #return render (request, 'cms/file_upload.html', dict(foo=321))

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
