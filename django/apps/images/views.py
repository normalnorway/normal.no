from django.http import HttpResponse


def index (request):
    return HttpResponse ('Hello world!')

#def foo (request):
#    return render_to_response('index.html', locals())
