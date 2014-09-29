# encoding: utf-8
import os
import datetime
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from website.settings import ROOT_DIR
from .models import Petition
from .forms import MemberForm


# @todo split in MemberTest and PettitionTest?
#       A: yes, that is recomended
class MyTestCase (TestCase):

    def test_petition_signup (self):
        data = {'name': u'frode frosk', 'city': u'ålesund', 'public': False, 'choice': u'c'}
        res = self.client.post (reverse('petition'), data)
        self.assertEqual (res.status_code, 200)
        obj = Petition.objects.values(*data.keys()).get(pk=1)
        self.assertEqual (data, obj)
        # self.assertEqual (res.context['objects'], data)
        # self.assertEqual (res.context['count'], 1)
        # @todo insert both public=True & False, then check that count=2
        #       and that only public=True is rendered
        # assertEqual (ctx['count'], 2)
        # assertEqual (len(ctx['objects']), 1)
        # @todo test name.title & city.title

    def test_new_member (self):
        filename = os.path.join (ROOT_DIR, 'db', 'newmembers')
        open (filename, 'w').close()    # clear file
        born = datetime.date (1977, 01, 20)
        data = {
            u'choice':   u'1',
            u'name':     u'Arne And',
            #u'born':     u'1977-01-20',
            #u'born':     u'20/01/77',
            # @todo test all date formats?
            u'born':     unicode (born.strftime('%d/%m/%y')),
            u'address1': u'Portveien 2',
            u'address2': u'',
            u'city':     u'Oslo',
            u'zipcode':  u'1234',
            u'email':    u'test@normal.no',
            u'phone':    u'',
            u'enrolled': unicode (datetime.date.today().strftime('%Y-%m-%d')),
            u'comment':  u'line one\nline two\nthe end',
            u'extra':    [u'1', u'3', u'5'],
        }
        res = self.client.post (reverse('enroll'), data)
        self.assertEqual (res.status_code, 200)
        # @note will get 200 even if form not valid. must check for validation error message
        obj = json.load (open(filename))
        data.update (born = unicode (born.strftime('%Y-%m-%d')))    # date is read back in iso format
        self.assertEqual (data, obj)

    def test_to_young_member (self):
        ''' Make sure we do not accept under age members '''
        now = datetime.date.today()
        born = datetime.date (now.year-18, now.month, now.day) + datetime.timedelta(days=1)
        form = MemberForm (dict(choice=u'1', name=u'name', born=born, address1='address1', city='city', zipcode=u'1234'))
        self.assertFalse (form.is_valid())
        self.assertTrue (form.errors.has_key('born'))
