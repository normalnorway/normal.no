# encoding: utf-8
import os
import datetime
import json
from django.test import TestCase, Client
from website.settings import ROOT_DIR

from .models import Petition
from .forms import MemberForm


# @todo split in MemberTest and PettitionTest?
class MyTestCase (TestCase):

    def setUp (self):
        self.client = Client()


    def test_petition (self):
        data = {'name': u'frode frosk', 'city': u'ålesund', 'public': False, 'choice': u'c'}
        res = self.client.post ('/opprop/', data)
        self.assertEqual (res.status_code, 200)
        obj = Petition.objects.values(*data.keys()).get(pk=1)
        self.assertEqual (data, obj)


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
        res = self.client.post ('/bli-medlem/', data)
        self.assertEqual (res.status_code, 200)
        # @note will get 200 even if form not valid. must check for validation error message
        obj = json.load (open(filename))
        data.update (born = unicode (born.strftime('%Y-%m-%d')))    # date is read back in iso format
        self.assertEqual (data, obj)


    def test_to_young_member (self):
        ''' Make sure we do not accept under age members '''
        now = datetime.date.today()
        born = datetime.date (now.year-18, now.month, now.day) + datetime.timedelta(days=1)
        data = {
            'choice':   u'1',
            'name':     u'Arne And',
            'born':     born,
            'address1': u'Portveien 2',
            'city':     u'Oslo',
            'zipcode':  u'1234',
        }
        form = MemberForm (data)
        self.assertFalse (form.is_valid())
        self.assertTrue (form.errors.has_key('born'))
