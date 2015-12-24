# encoding: utf-8
# $ ./manage.py test tests
from django.test import TestCase, Client

# @todo insert test data

class TestUrls (TestCase):
    def _http_status (self, url):
        return self.client.get (url).status_code
        #return self.client.head (url).status_code

    def test_home (self):
        self.assertEqual (200, self._http_status ('/'))
    def test_nyhetsbrev (self):
        self.assertEqual (200, self._http_status ('/nyhetsbrev/'))
    def test_bli_medlem (self):
        self.assertEqual (200, self._http_status ('/bli-medlem/'))
    def test_opprop (self):
        self.assertEqual (200, self._http_status ('/opprop/'))
    def test_nettguide (self):
        self.assertEqual (200, self._http_status ('/nettguide/'))
    def test_nyhetsbrev_1 (self):
        self.assertEqual (200, self._http_status ('/nyhetsbrev/1/'))
    # These are in cms.Pages
#    def test_om_normal (self):
#        self.assertEqual (200, self._http_status ('/om-normal/'))
#    def test_on_normal_ledelsen (self):
#        self.assertEqual (200, self._http_status ('/om-normal/ledelsen/'))
#    def test_stott (self):
#        self.assertEqual (200, self._http_status (u'/støtt/'))
#    def test_om_cannabis (self):
#        self.assertEqual (200, self._http_status ('/om-cannabis/'))
#    def test_faq (self):
#        self.assertEqual (200, self._http_status ('/faq/'))
#    def test_medisin (self):
#        self.assertEqual (200, self._http_status ('/medisin/'))
#    def test_visjon (self):
#        self.assertEqual (200, self._http_status ('/visjon/'))
#    def test_europa (self):
#        self.assertEqual (200, self._http_status ('/europa/'))



class TestRedirects (TestCase):
    '''Test all (permantent) redirect views/urls'''
    # @todo use assertRedirects (response, expected_url, status_code=301);
#    response = self.client.head ('/medlem/')
#    self.assertRedirects (response, '/bli-medlem')
    def _test_medlem (self):
        self.assertRedirects (self.client.head ('/medlem/'), '/bli-medlem')

    def test_medlem (self):
        res = self.client.head ('/medlem/')
        self.assertEqual (res.status_code, 301)
        self.assertTrue (res['location'].endswith ('/bli-medlem/'))
    def test_rss (self):
        res = self.client.head ('/rss/')
        self.assertEqual (res.status_code, 301)
        self.assertTrue (res['location'].endswith ('/nyheter/rss/'))
    def test_gruppesoksmaal (self):
        res = self.client.head (u'/gruppesøksmaal/')
        self.assertEqual (res.status_code, 301)
        self.assertTrue (res['location'].endswith ('/sider/gruppesoksmaal/'))
    def test_frivillig (self):
        res = self.client.head ('/frivillig/')
        self.assertEqual (res.status_code, 301)
        self.assertTrue (res['location'].endswith ('/sider/frivillig/'))
    '''
    def test_ (self):
        res = self.client.head ('')
        self.assertEqual (res.status_code, 301)
        self.assertTrue (res['location'].endswith (''))
    '''
