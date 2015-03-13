from django.test import TestCase, Client
from django.core import urlresolvers
from website import urls

# TODO
# nyheter/  (included urls)
# own testcase per url (better to manually add?)

class GlobalTestCase (TestCase):
    def setUp (self):
        self.client = Client()

    def test_views (self):
        """Check that all views from website.urls returns http success"""
        for obj in urls.urlpatterns:
            if isinstance (obj, urlresolvers.RegexURLPattern):
                if obj.name and 'password_reset' in obj.name: continue
                assert obj.regex.pattern[-1] == '$'
                # @todo don't just blindly chop of first and last char
                #       replace first '^' with '/'
                #       chop last if '$'
                url = '/' + obj.regex.pattern[1:-1] # drop first and last char (regex anchors)
                res = self.client.head (url)
                if obj.callback.__name__ == 'RedirectView':
                    self.assertEqual (res.status_code, 301)
                else:
                    self.assertEqual (res.status_code, 200)

            elif isinstance (obj, urlresolvers.RegexURLResolver):
                # @todo recurse on o.url_patterns, but skip if o.namespace == 'admin'
                pass
