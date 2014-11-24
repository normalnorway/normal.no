# encoding: utf-8
"""
Test that all urls/views on normal.no is working. E.g., returning a
2xx status code.

Use this after deploying to test site; then can rollback if not ok.
"""

PREFIX = 'http://normal.no'


import unittest
import httplib
from urlparse import urlsplit


#connection = httplib.HTTPConnection ('normal.no')
# then do multiple requests with keep-alive


# @todo handle query string
# @todo timeout. @see https://docs.python.org/2/library/httplib.html
def get_http_status (urlstr):
    #print 'Checking', urlstr
    url = urlsplit (PREFIX + urlstr)
    #assert url.query=='' and url.fragment==''
    c = httplib.HTTPConnection (url.hostname)
    c.request ('HEAD', url.path)
    return c.getresponse().status



class TestLiveSite (unittest.TestCase):
    def test_url_0 (self): self.assertEqual (200, get_http_status ('/'))
    def test_url_1 (self): self.assertEqual (200, get_http_status ('/om-normal/'))
    def test_url_2 (self): self.assertEqual (200, get_http_status ('/bli-medlem/')) # @todo test /medlem/ alias?
    def test_url_3 (self): self.assertEqual (200, get_http_status ('/støtt/'))
    def test_url_4 (self): self.assertEqual (200, get_http_status ('/nyhetsbrev/'))
    def test_url_5 (self): self.assertEqual (200, get_http_status ('/opprop/'))
    def test_url_6 (self): self.assertEqual (200, get_http_status ('/nyheter/arkiv/'))
    def test_url_7 (self): self.assertEqual (200, get_http_status ('/nettguide/'))
    def test_url_8 (self): self.assertEqual (200, get_http_status ('/om-cannabis/'))
    def test_url_9 (self): self.assertEqual (200, get_http_status ('/faq/'))


if __name__ == '__main__':
    unittest.main()
