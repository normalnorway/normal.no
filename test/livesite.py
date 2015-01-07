# encoding: utf-8
"""
Test that all urls/views on normal.no is working.
"""

import unittest
import httplib

connection = httplib.HTTPConnection ('normal.no', timeout=5)

def get_http_status (path):
    connection.request ('HEAD', path)
    res = connection.getresponse()
    res.read()
    return res.status


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
    def test_url_10 (self): self.assertEqual (200, get_http_status ('/nyheter/rss/'))
    def test_url_11 (self): self.assertEqual (301, get_http_status ('/rss/'))   # redirects to /nyheter/rss/


if __name__ == '__main__':
    unittest.main()
