# encoding: utf-8

import re
import operator
from mailchimpapi import MailChimpBase
from datetime import datetime

# MailChimp code specific for normal.no

class MailChimp (MailChimpBase):
    '''Add customization for normal.no'''

    _RE_NEWSLETTER = re.compile (r'^.*#(\d+)$')

    # Title lookup table. Use this to override individual newsletter titles.
    _TITLE_LUT = {
        '8065fc1366': u'Medisinsk cannabis: forskningsprosjekt',
        '45feb88ec0': u'Valgkamp: Vil du stå på stand med Normal i Oslo?',
        '7c20007c36': u'Referat: Torsdagsmøte 8/5/2014',
    }

    def _get_title (self, item):
        # Fixup newsletter title so its more consistent.
        title = self._TITLE_LUT.get (item['id'], None)
        if title: return title
        match = self._RE_NEWSLETTER.match (item['settings']['title'])
        if match: return 'Nyhetsbrev #' + match.group(1)
        return item['settings']['title']    # @todo log/warn?

    def _convert_date (self, data, field='date'):
        '''Convert field to Python datetime.date object'''
        # Note: Will truncate time and only returns date() (not datetime).
        for item in data:
            item[field] = datetime.strptime (item.get(field), '%Y-%m-%dT%H:%M:%S+00:00').date()

    def get_campaigns (self):   # @todo count
        '''Get all (sendt) campaigns'''
        #_fields = ['id', 'send_time', 'settings.title', 'settings.subject_line', 'recipients.list_id']
        #fields = ['campaigns.'+field for field in _fields]
        fields = ['campaigns.'+field for field in ('id', 'send_time', 'settings.title')]
        data = self.get ('/campaigns', count=250, status='sent', fields=fields) # Note: count=10 by default
        data = data['campaigns']
        assert len(data) < 250, 'TODO: add pagination' # @todo warning.warn, log or mail_admin

        self._convert_date (data, 'send_time') # send_time: str -> datetime

        for item in data:
            item['title'] = self._get_title (item)
            del item['settings']

        data.sort (reverse=True, key = operator.itemgetter ('send_time'))
        return data
