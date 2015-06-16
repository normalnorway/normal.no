import ConfigParser

# Possible improvements:
# * Get default values from the environment
# * Get default values from this file
# @todo log/error if site.ini exists, but not readable


# These are the defaults if not defined in the inifile ('site.ini')
# Note: Must use correct Python type here.
# Q: Should default passed to getters override DEFAULTS?
#DEFAULTS = \
#{
#    'main.debug':    True,  # @todo default to False if site.ini exists?
#}


class SiteConfig (object):

    def __init__ (self, filename):
        self.cfg = ConfigParser.SafeConfigParser()
        ret = self.cfg.read (filename)
        #if not ret: print "WARNING: Can't load: " + filename
        self._loaded = bool (ret)
        # note: filename can also be list of filenames

#    def exists (self):  # rename is_loaded or loaded?
#        """Return True if the configuration file was found"""
#        return self._loaded

#    def has_option (self, path):
#        return self._lookup (path)[-1]

#    def _lookup (self, path, default=None):
#        if '.' in path:
#            sec, key = path.split ('.')
#        else:
#            sec, key = 'main', path
#        #sec, key = path.split ('.') if '.' in path else ('main', path)
#        if self.cfg.has_option (sec, key):
#            return self.cfg.get (sec, key)
#        if default: return default
#        raise KeyError (path)

#    def _default (self, path):
#        #return DEFAULTS.get (path)          # might raise KeyError
#        #return DEFAULTS.get (path, None)
#        if not DEFAULTS.has_key (path): return None
#        return DEFAULTS[path]

    # Note: If dot is missing from path, then 'main.' is prepended
    def _lookup (self, path):
        sec, key = path.split ('.') if '.' in path else ('main', path)
        return sec, key, self.cfg.has_option (sec, key)

    def _get (self, path, default):
        sec, key, haveit = self._lookup (path)
        if haveit: return self.cfg.get (sec, key)
        if default is not None: return default
        raise KeyError (path)

    def get (self, path, default=None):
        return self._get (path, default)

    # @todo don't duplicate code from _get. can pass self.cfg.get
    #       or self.cfg.getbool as getter arg to _get()
    def getbool (self, path, default=None):
        sec, key, haveit = self._lookup (path)
        if haveit: return self.cfg.getboolean (sec, key)
        if default is not None: return default
        raise KeyError (path)

    #def getint (self, path, default=None):
    #def getfloat (self, path, default=None):



# This is only used for testing.
if __name__ == '__main__':
    import os
    filename = os.path.dirname (__file__)
    filename = os.path.join (filename, os.path.pardir, os.path.pardir, 'site.ini')
    cfg = SiteConfig (filename)
#    assert cfg.is_loaded()
    assert cfg.getbool ('main.debug') is True   # site.ini has debug=True
    assert cfg.getbool ('debug', False) is True
    # main is the default section
    assert cfg.get ('foobar', 222) == 222   # ok; since have default (222)
    #print cfg.get ('foobar')       # fails; since default is missing
    #print cfg.get ('foobar', None) # fails; since default can't be None
    assert cfg.get ('main.foo', 333) is 333
    try:
        print cfg.get ('main.foo')
    except KeyError as ex:
        assert ex.message is 'main.foo'
    print 'Test OK'
