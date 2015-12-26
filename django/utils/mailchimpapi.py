r"""
Very simple wrapper around MailChimp REST API V3.

Only the stuff need on normal.no is implemented:
1) Get all campaigns
2) Get one campaign (not implemented yet)
"""

# http://developer.mailchimp.com/documentation/mailchimp/guides/get-started-with-mailchimp-api-3/
# http://developer.mailchimp.com/documentation/mailchimp/reference/overview/
# https://us1.api.mailchimp.com/playground/
#
# The root directory for the API includes a map of all available resources and
# their subresources: https://<dc>.api.mailchimp.com/3.0
#
# https://<dc>.api.mailchimp.com/3.0/lists
# https://<dc>.api.mailchimp.com/3.0/lists/{list_id}.
#
# There are 2 authentication methods for the API:
# HTTP Basic authentication and OAuth2.
#
# Request data is passed to the API by POSTing JSON objects.

from httplib import HTTPSConnection
from urlparse import urlparse
from urllib import urlencode
from base64 import b64encode
import json

ENDPOINT = 'https://%s.api.mailchimp.com/3.0/'

# Update: Not needed. At least not for GET requests ...
#HEADERS = {
#    'Content-type': 'application/json; charset=utf-8',
#    'Accept':       'application/json',
#}


class ApiError (RuntimeError):
    pass


def dict_to_query_string (kwargs):
    out = {}
    for key,val in kwargs.items():
        if isinstance (val, list):
            out[key] = ','.join (val)
        elif isinstance (val, (int, long)):
            out[key] = str(val)     # needed?
        else:
            assert isinstance (val, basestring), 'FIXME'
            out[key] = val
    return urlencode (out)


class MailChimpBase (object):
    def __init__ (self, apikey, debug=False, timeout=10):
        self.debug = debug
        #urlobj = urlparse (ENDPOINT % apikey.split('-')[-1])
        urlobj = urlparse (ENDPOINT % apikey[-3:])
        self.base_path = urlobj.path
        self.http = HTTPSConnection (urlobj.hostname, timeout=timeout)
        #if debug: self.http.set_debuglevel (1)
        self.headers = dict (Authorization = 'Basic ' + b64encode('nil:'+apikey))

    def get (self, path, **kwargs):
        '''Generic HTTP GET call'''
        url = self.base_path + path + '?' + dict_to_query_string (kwargs)
        if self.debug: print 'GET', url
        self.http.request ('GET', url, headers=self.headers)

        response = self.http.getresponse()
        if response.status == 200:
            return json.loads (response.read())
        if not self.debug:
            raise ApiError()    # @todo add error context. HTTPResponse.reason

        print 'API-ERROR'
        from pprint import pprint
        pprint (json.loads(response.read()))
        exit(1)
