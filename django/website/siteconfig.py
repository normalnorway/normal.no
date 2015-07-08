import os
import ConfigParser

# Possible improvements:
# * Get default values from the environment

class SiteConfig (object):

    def __init__ (self, filename):
        '''Load an ini file'''
        if os.path.exists (filename) and not os.access (filename, os.R_OK):
            raise IOError ('Can not read: ' + os.path.realpath (filename))
            #raise IOError ('EACCES', filename, 'Can not read')
        self.cfg = ConfigParser.SafeConfigParser()
        ret = self.cfg.read (filename) # note: can be list of filenames
        self._loaded = bool (ret)
        #if not ret: print "WARNING: Can't load: " + filename

    def is_loaded (self):
        """Return True if the configuration file was found and loaded"""
        return self._loaded

    def has_option (self, path):
        return self._lookup (path)[-1]

    # Note: If dot is missing from path, then 'main.' is prepended
    def _lookup (self, path):
        sec, key = path.split ('.') if '.' in path else ('main', path)
        return sec, key, self.cfg.has_option (sec, key)

    def _get (self, path, getter, default):
        section, key, found = self._lookup (path)
        if found: return getter (section, key)
        if default is not None: return default
        raise KeyError (path)

    def get (self, path, default=None):
        return self._get (path, self.cfg.get, default)

    def getbool (self, path, default=None):
        if default is not None: default = bool(default)
        return self._get (path, self.cfg.getboolean, default)

    def getint (self, path, default=None):
        if default is not None: default = int(default)
        return self._get (path, self.cfg.getint, default)

    def getfloat (self, path, default=None):
        if default is not None: default = float(default)
        return self._get (path, self.cfg.getfloat, default)



# Only used for testing
if __name__ == '__main__':
    filename = os.path.dirname (__file__)
    filename = os.path.join (filename, os.path.pardir, os.path.pardir, 'site.ini')
    cfg = SiteConfig (filename)
    assert cfg.is_loaded()
    assert cfg.has_option ('debug')
    assert cfg.has_option ('main.debug')
    assert not cfg.has_option ('void')
    assert cfg.getbool ('main.debug') is True   # site.ini has debug=True
    assert cfg.getbool ('debug', False) is True
    assert cfg.get ('foobar', 222) == 222   # ok; since have default (222)
    #print cfg.get ('foobar')
    assert cfg.get ('main.foo', 333) == 333
    try:
        print cfg.get ('main.foo')  # fails; since default is missing
    except KeyError as ex:
        assert ex.message == 'main.foo'
    else:
        assert False
    try:
        print cfg.get ('foobar', None) # fails; since default can't be None
    except KeyError as ex:
        pass
    else:
        assert False
    assert cfg.getbool ('foo', 1) is True
    assert cfg.getbool ('bar', '0') is True
    assert cfg.getbool ('baz', 0) is False
    print 'Test OK'
