from django import template
from apps.content.models import Content

register = template.Library()

@register.simple_tag
def get_content (key):
    try:
        return Content.objects.get (name=key).content
    except Content.DoesNotExist:
        return '[ERROR: Unknown content block: %s]' % key
    # Note: returned string is auto marked as safe
