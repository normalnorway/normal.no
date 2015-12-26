"""
Global views -- i.e., don't tied to any app/model.
"""

from core.shortcuts import render_to


@render_to ('index.html')
def index (request):
    return {}



from utils.mailchimp import MailChimp
from django.conf import settings

mailchimp = MailChimp (settings.MAILCHIMP_API_KEY)

@render_to ('newsletter.html')
def newsletter (request):
    return {'campaigns': mailchimp.get_campaigns} # note: lazy evaluation
