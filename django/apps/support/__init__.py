import json
from website.settings import rootdir

# File object to write new members to. Use add_new_member() instead
# of directly writing to this file.
try:
    _new_member_fp = open (rootdir ('db', 'newmembers'), 'a')
except IOError, ex:
    import logging
    logging.critical ('Can not open newmembers file: ' + ex.strerror)
    #logging.critical ('Can not open newmembers file: ' + str(ex))
    # @todo pass exception


# @todo move to core.members?
# @todo filter/remove empty elements?
def add_new_member (data):
    '''Add a new member. Data is a dict'''
    data['born'] = data['born'].strftime ('%F') # json don't handle datetime objects, so convert to string
    #data['born'] = str (data['born']) # does the same as above (i think)
    fp = _new_member_fp
    json.dump (data, fp)
    fp.write ('\n')
    fp.flush()
