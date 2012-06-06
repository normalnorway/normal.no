from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from apps.files.models import File
from apps.files.forms import FileForm
# can use relative paths:
# from .models import File
# from .forms import FileForm

#from apps.files import forms
# forms.EditorUploadForm()

# response['Content-Disposition'] = 'attachment; filename=foo.xls'



# Not a real view. Used to upload images from Dojo Editor.
# http://dojotoolkit.org/reference-guide/1.7/dojox/editor/plugins/LocalImage.html
# XXX: uploaded filename is used on server (name conflict & security problem?)
# @todo Use an EditorUploadedFile class instead. This will fix name
#       conflicts, and record the files in the database
@csrf_exempt
def upload (request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden ("Forbidden")
    if request.method != 'POST':
        return HttpResponse ()  # log?

    # Save image
    #fp = open (settings.MEDIA_ROOT + "editor/" + request.FILES['uploadedfile'].name, "wb")
    f = request.FILES['uploadedfile']
    fcommon = "editor/" + f.name
    filename = settings.MEDIA_ROOT + fcommon
    fp = open (filename, "wb")
    for chunk in f.chunks():
        fp.write (chunk)

    from PIL import Image
    import json
    # @todo from django.utils.simplejson import JSONEncoder

    # Get metadata (and return to server)
    img = Image.open (filename)
    w,h = img.size
    data = {
        'file':     settings.MEDIA_URL[1:] + fcommon,
        'name':     f.name,
        'width':    w,
        'height':   h,
        'type':     img.format.lower(),
        'size':     f.size,
    }
    print data
    print "<textarea>" + json.dumps(data) + "</textarea>"
    return HttpResponse ("<textarea>" + json.dumps(data) + "</textarea>")
#    "<textarea>{'file':'%s', 'name':'%s', 'width':%d, 'height':%d 'type':%s, 'size':%d}</textarea>"




@login_required
def list (request):
    p = request.user.get_profile()
    print type(p)
    print p
    return HttpResponse ()

    if request.method == 'POST':
        form = FileForm (request.POST, request.FILES)
        if form.is_valid(): 
            #file = form.fields['file']     # field from the form

#            file = request.FILES['file']
#            print type(file)
#            print file.content_type

#            f = File (file = request.FILES['file'])
#            print f.file.name
#            print f.file.size
#            print f.file.path
#            print f.file.url
            # Q: mime-type / content type
            return HttpResponse('File was posted')
    else:
        form = FileForm()

    # Render list view
    return render (request, 'files/list.html', {
        'files':    File.objects.all(),
        'form':     form,
    });



# @todo feedback: file uploaded ok
def list_old (request):
    # Handle file upload
    if request.method == 'POST':
        form = FileForm (request.POST, request.FILES)
        if form.is_valid():
            f = File (file = request.FILES['file'])
            f.name = 'fixme'
            f.save()
            # redirect so not posting twice(?) try without
            return HttpResponseRedirect ('/files/list')
            # q: where to import reverse from? django.urls?
            #return HttpResponseRedirect (reverse('apps.files.views.list'))
        else:
            raise 'FormNotValid'

    # Render list view
    return render (request, 'files/list.html', {
        'files':    File.objects.all(),
        'form':     FileForm(),
    })
