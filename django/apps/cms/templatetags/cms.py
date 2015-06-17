from django import template
from django.core.urlresolvers import reverse
from django.utils.http import urlquote_plus
from apps.cms.models import Content

register = template.Library()

@register.simple_tag (takes_context=True)
def cms_content (context, key):
    try:
        obj = Content.objects.get (name=key)
    except Content.DoesNotExist:
        return '[ERROR: Unknown content block: %s]' % key

    request = context['request']
    if not request.user.has_perm ('cms.change_content'):
        return obj.content

    url = reverse ('content-update', args=[obj.pk])
    url += '?next=%s' % urlquote_plus (request.get_full_path())

    return obj.content + '<a href="%s" accesskey="e" class="admin-edit-link">Rediger</a>' % url
    # Note: returned string is automatically marked as safe
