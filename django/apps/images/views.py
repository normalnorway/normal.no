from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.images.models import EditorImage


@csrf_exempt
def editor_upload (request):
    assert (request.user.is_authenticated())
    assert (request.method == 'POST')

    # Save
    # @note EditorImage() will raise TypeError if file is not an image
    # f.content_type.split('/')[0]
    f = request.FILES['uploadedfile']
    image = EditorImage (file = f)
    image.save()

    # Return metadata to Dojo.Editor
    import os.path
    import json
    data = {
        'file':     image.file.url[1:],
        'width':    image.file.width,
        'height':   image.file.width,
        'type':     os.path.splitext (f.name)[1][1:], # f.name.split(".")[-1]
        'name':     f.name,
        'size':     f.size,
    }
    return HttpResponse ("<textarea>" + json.dumps(data) + "</textarea>")
