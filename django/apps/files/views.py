from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from apps.files.models import File
from apps.files.forms import FileForm


def list (request):
    # Handle file upload
    if request.method == 'POST':
        form = FileForm (file = request.FILES)
        #form = FileForm (request.POST)
        if form.is_valid():
            f = File (file = request.FILES['file'])
            f.save()
            return HttpResponseRedirect (reverse('apps.files.views.list'))
        else:
            raise 'FormNotValid'

    # Render list view
    ctx = {
        'files':    File.objects.all(),
        'form':     FileForm(),
    }
    return render_to_response ('files/list.html', ctx,
            context_instance = RequestContext(request))
#    return render_to_response ('files/list.html',
#            { 'files': Files.objects.all(), 'form': FileForm(), },
#            context_instance = RequestContext(request))
