import os
import json
from website.settings import ROOT_DIR


# File object to write new members to. Use add_new_member() instead
# of directly writing to this file.
new_member_fp = open (os.path.join (ROOT_DIR, 'db', 'newmembers'), 'a')


# @todo move to core.members?
# @todo filter/remove empty elements?
def add_new_member (data):
    '''Add a new member. Data is a dictionary'''
    data['born'] = data['born'].strftime ('%F') # json don't handle datetime objects, so convert to string
    fp = new_member_fp
    json.dump (data, fp)
    fp.write ('\n')
    fp.flush()
