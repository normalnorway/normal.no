from django import template
from django.core.urlresolvers import reverse
from apps.content.models import Content

register = template.Library()

@register.simple_tag (takes_context=True)
def get_content (context, key):
    try:
        obj = Content.objects.get (name=key)
    except Content.DoesNotExist:
        return '[ERROR: Unknown content block: %s]' % key

    if not context['request'].user.is_staff:
        return obj.content

    #return EDIT_BUTTON_HTML % reverse ('admin:content_content_change', args=[obj.pk]) + obj.content
    return obj.content + '<a href="%s" class="admin-edit-link">Rediger</a>' % \
                reverse ('admin:content_content_change', args=[obj.pk])

    # Note: returned string is auto marked as safe
