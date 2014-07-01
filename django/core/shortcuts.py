from django.shortcuts import render

# @todo get_http_page, returns tuple (status/headers, content)

# @todo rename get_http_status (move to core.http?)
# @todo what about fragments? normal.no/#doner
# http://docs.python-requests.org/en/latest/
import httplib
import urlparse
def get_http_status (urlstr):
    url = urlparse.urlsplit (urlstr)
    assert not url.query    # q: what to do with query string?
    try:
        conn = httplib.HTTPConnection (url.hostname)
        conn.request ('HEAD', url.path)
        return conn.getresponse().status
    except StandardError:
        return None     # @todo return 500 instead of None?



# Stolen (and modified) from: https://djangosnippets.org/snippets/821/
def render_to (template):
    """
    Decorator for Django views that sends returned dict to the render
    function with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter.

    Parameters:
     - template: Template to use. It can be prefixed with app-name,
                 e.g., @render_to ('myapp:mytemplate.html').
    """
    template = template.replace (':', '/', 1)   # app prefix
    def renderer (func):
        def wrapper (request, *args, **kw):
            output = func (request, *args, **kw)
            if isinstance (output, (list, tuple)):
                return render (request, output[1], output[0])
            elif isinstance (output, dict):
                return render (request, template, output)
            return output
        return wrapper
    return renderer
