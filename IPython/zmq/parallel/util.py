"""some generic utilities"""
import re

class ReverseDict(dict):
    """simple double-keyed subset of dict methods."""
    
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self._reverse = dict()
        for key, value in self.iteritems():
            self._reverse[value] = key
    
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self._reverse[key]
    
    def __setitem__(self, key, value):
        if key in self._reverse:
            raise KeyError("Can't have key %r on both sides!"%key)
        dict.__setitem__(self, key, value)
        self._reverse[value] = key
    
    def pop(self, key):
        value = dict.pop(self, key)
        self.d1.pop(value)
        return value
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    

def validate_url(url):
    """validate a url for zeromq"""
    if not isinstance(url, basestring):
        raise TypeError("url must be a string, not %r"%type(url))
    url = url.lower()
    
    proto_addr = url.split('://')
    assert len(proto_addr) == 2, 'Invalid url: %r'%url
    proto, addr = proto_addr
    assert proto in ['tcp','pgm','epgm','ipc','inproc'], "Invalid protocol: %r"%proto
    
    # domain pattern adapted from http://www.regexlib.com/REDetails.aspx?regexp_id=391
    # author: Remi Sabourin
    pat = re.compile(r'^([\w\d]([\w\d\-]{0,61}[\w\d])?\.)*[\w\d]([\w\d\-]{0,61}[\w\d])?$')
    
    if proto == 'tcp':
        lis = addr.split(':')
        assert len(lis) == 2, 'Invalid url: %r'%url
        addr,s_port = lis
        try:
            port = int(s_port)
        except ValueError:
            raise AssertionError("Invalid port %r in url: %r"%(port, url))
        
        assert pat.match(addr) is not None, 'Invalid url: %r'%url
        
    else:
        # only validate tcp urls currently
        pass
    
    return True


def validate_url_container(container):
    """validate a potentially nested collection of urls."""
    if isinstance(container, basestring):
        url = container
        return validate_url(url)
    elif isinstance(container, dict):
        container = container.itervalues()
    
    for element in container:
        validate_url_container(element)