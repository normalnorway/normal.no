from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Helper function to store an uploaded file
import os
from website.settings import MEDIA_ROOT, MEDIA_URL
# @todo rename f => fileobj
def store_upload (f, name, upload_to=''):
    '''Stores the UploadedFile object. Returns the media URL'''
    path = os.path.join (MEDIA_ROOT, upload_to)

    try: os.makedirs (path)
    except OSError, ex:
        if ex.errno != os.errno.EEXIST: raise

    filename = os.path.join (path, name) # @todo check if exists (os.path.exists (filename)), or give unique name based on content
    url = os.path.join (MEDIA_URL, upload_to, name)
    # file is TemporaryUploadedFile or InMemoryUploadedFile
    # file.{name,size,content_type,charset
    try:
        os.rename (f.temporary_file_path(), filename)
    except AttributeError:
        with open (filename, 'wb+') as fp:
            for chunk in f.chunks():
                fp.write (chunk)
    return url


# @todo enable csrf, and drop this
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
@login_required
def upload (request):
    # @todo check if file exists
    #upload = request.FILES['tinymce-file-input']   # hardcoded
    upload = request.FILES[request.FILES.keys()[0]] # @todo handle multi?
    url = store_upload (upload, upload.name, 'tinymce')
    return HttpResponse ('OK ' + url)
