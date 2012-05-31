from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from apps.files.models import File
from apps.files.forms import FileForm


# Not a real view. Just stores the uploaded file and return its URL
# (To handle uploads from rich editor (or other external component))
#@csrf_exempt
@login_required
def upload (request):
    pass



@login_required
def list (request):
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
    return render_to_response ('files/list.html', {
        'files':    File.objects.all(),
        'form':     form,
        }, context_instance = RequestContext(request))



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
    ctx = {
        'files':    File.objects.all(),
        'form':     FileForm(),
    }
    return render_to_response ('files/list.html', ctx,
            context_instance = RequestContext(request))
#    return render_to_response ('files/list.html', ctx)
#    Your template will be passed a Context instance by default.

#    return render_to_response ('files/list.html',
#            { 'files': Files.objects.all(), 'form': FileForm(), },
#            context_instance = RequestContext(request))
