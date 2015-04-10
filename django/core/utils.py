# Not in use (yet)
# But collect usefull stuff here


def dict_remove_empty (data):
    """Remove empty values from a dict. A copy is returned"""
    return dict((k, v) for k, v in data.iteritems() if v)

