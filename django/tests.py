from django.test import TestCase, Client
from django.core import urlresolvers
from website import urls


class GlobalTestCase (TestCase):
    def setUp (self):
        self.client = Client()

    def test_views (self):
        ''' Check that all views from website.urls returns http success '''
        for o in urls.urlpatterns:
            if isinstance (o, urlresolvers.RegexURLPattern):
                url = '/' + o.regex.pattern[1:-1]
                res = self.client.head (url)
                #print res.status_code, url
                self.assertEqual (res.status_code, 200)
            elif isinstance (o, urlresolvers.RegexURLResolver):
                pass
                # @todo recurse on o.url_patterns, but skip if o.namespace == 'admin'
