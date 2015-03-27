from django import template
from django.core.urlresolvers import reverse
from django.utils.http import urlquote_plus
from apps.content.models import Content

register = template.Library()

@register.simple_tag (takes_context=True)
def get_content (context, key):
    try:
        obj = Content.objects.get (name=key)
    except Content.DoesNotExist:
        return '[ERROR: Unknown content block: %s]' % key

    request = context['request']
    if not request.user.has_perm ('content.change_content'):
        return obj.content

    url = reverse ('edit-block', args=[obj.pk])
    url += '?back=%s' % urlquote_plus (request.get_full_path())

    return obj.content + '<a href="%s" class="admin-edit-link">Rediger</a>' % url
    # Note: returned string is automatically marked as safe
