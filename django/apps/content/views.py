"""
http://stackoverflow.com/questions/4011332/extend-flatpages-for-a-specific-application
Using own form to edit flatpages
"""

from django.views.generic.edit import UpdateView
from django.contrib.flatpages.models import FlatPage
from forms import PageEditForm

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

# When migrating away from flatpages, then don't need custom form and
# can just do this:
#class PageEditView (UpdateView):
#    model = ContentPages
#    fields = 'title', 'content'


#from django.utils.decorators import method_decorator
#from django.contrib.auth.decorators import login_required

class PageEditView (UpdateView):
    model = FlatPage
    form_class = PageEditForm
    template_name = 'flatpages/edit.html'

#    def _check_perm (self, user, obj_pk):
#        if user.pk == 8: return obj_pk not in (25,26)  # user can only edit this object
#        return user.has_perm ('flatpages.change_flatpage')

#    @method_decorator (login_required)
    def dispatch (self, *args, **kwargs):
        request = args[0]
        pk = int(kwargs['pk'])

#        if not self._check_perm (request.user, pk):
#            raise PermissionDenied()
#        return super (PageEditView, self).dispatch (*args, **kwargs)

        # Hack: allow to edit of FlatPage.pk=25+26 for User.pk=8 (bjorn)
        if request.user.pk == 8:
            if pk not in (25,26):
                return HttpResponseForbidden ('<h1>403 Forbidden</h1><p>Dette har du ikke lov til :)')
            return super (PageEditView, self).dispatch (*args, **kwargs)

        if not request.user.has_perm ('flatpages.change_flatpage'):
            raise PermissionDenied()
        return super (PageEditView, self).dispatch (*args, **kwargs)
