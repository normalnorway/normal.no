from django import template
from django.core.urlresolvers import reverse
from django.utils.http import urlquote_plus
from apps.cms.models import Content

register = template.Library()

@register.simple_tag (takes_context=True)
def cms_content (context, key):
    request = context['request']
    can_edit = request.user.has_perm ('cms.change_content')
    try:
        obj = Content.objects.get (name=key)
    except Content.DoesNotExist:
        if not can_edit: return ''
        url = reverse ('admin:cms_content_add') + '?name=' + key
        return '<div class="small gray"><a href="%s">[add text]</a></div>' % url

    if not can_edit:
        return obj.content

    url = reverse ('content-update', args=[obj.pk])
    url += '?next=%s' % urlquote_plus (request.get_full_path())
    return obj.content + '<a href="%s" accesskey="e" class="admin-edit-link">Rediger</a>' % url
    # Note: returned string is automatically marked as safe
