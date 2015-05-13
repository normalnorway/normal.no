import ConfigParser

# @todo don't make debug default to true if site.ini exists

# Also get defaults from the environment?
#DEFAULT_SECRET_KEY = 'secret'
#SECRET_KEY = os.environ.get ('SECRET_KEY', DEFAULT_SECRET_KEY)


# These are the defaults if not defined in 'site.ini'
# Note: Must use correct Python type here.
DEFAULTS = \
{
    'main.debug':    True,
#    'main.secret':   'x' * 50,
}

class SiteConfig (object):

    def __init__ (self, filename):
        self.cfg = ConfigParser.SafeConfigParser()
        self.cfg.read (filename)
        # @todo log if file don't exists

    def _foo (self, path):
        if '.' in path:
            sec, key = path.split ('.')
        else:
            sec, key = 'main', path
        return sec, key, self.cfg.has_option (sec, key)

    def _get (self, path, default=None):
        if '.' in path:
            sec, key = path.split ('.')
        else:
            sec, key = 'main', path
        if self.cfg.has_option (sec, key):
            return self.cfg.get (sec, key)
        val = DEFAULTS.get ('%s.%s' % (sec,key), default)
        #val = DEFAULTS.get (key, default)  # try without prefix
        if not val: raise KeyError (path)  # @todo log and default to None?
        return val

#    def _default (self, sec, key, default):
#        val = DEFAULTS.get ('%s.%s' % (sec,key), default)
#        if not val: raise KeyError (sec+'.'+key)

    # Q: Should default passed to getters override DEFAULTS?

    def get (self, path, default=None):
        return self._get (path, default)

    def getbool (self, path, default=None):
        sec, key, haveit = self._foo (path)
        if haveit: return self.cfg.getboolean (sec, key)
        if default: return default
        return DEFAULTS.get ('%s.%s' % (sec,key)) # might raise KeyError



if __name__ == '__main__':
    cfg = SiteConfig ('../../site.ini')
    print cfg._get ('debug')
    print cfg._get ('main.debug')
    print cfg._get ('foo', 111)
    print cfg._get ('main.foo', 222)
    print cfg._get ('main.foo')
