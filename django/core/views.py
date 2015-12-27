"""
Global views -- i.e., don't tied to any app/model.
"""

from core.shortcuts import render_to


@render_to ('index.html')
def index (request):
    return {}



## /newsletter/

from utils.mailchimp import MailChimp
from django.conf import settings

#mailchimp = None
#if settings.MAILCHIMP_API_KEY:
#    mailchimp = MailChimp (settings.MAILCHIMP_API_KEY)

mailchimp = MailChimp (settings.MAILCHIMP_API_KEY) if settings.MAILCHIMP_API_KEY else None
# or use config.mailchimp in core/context_processors.py (like piwik) ?
# or: MailChimp(None) => all operations is nop
# @todo log/warn missing api-key?

@render_to ('newsletter.html')
def newsletter (request):
    return {'campaigns': mailchimp.get_campaigns if mailchimp else None}
