import inspect, os, sys
from itertools import chain

def _import(module_name):
    __import__(module_name)
    return sys.modules[module_name]

def load_submodules(parent_module_name):
    """
    import and return a list of all submodules of the named module
    """
    parent = _import(parent_module_name)
    pdir = os.path.dirname(parent.__file__)

    ret = []

    for x in os.listdir(pdir):
        submodule_name = None
        if not os.path.isdir(os.path.join(pdir, x)) and x.endswith('.py') and x != '__init__.py':
            submodule_name = os.path.splitext(x)[0]
        elif os.path.exists(os.path.join(pdir, x, '__init__.py')):
            submodule_name = x
        else:
            continue
        
        ret.append(_import(parent_module_name+'.'+submodule_name))

    return ret

def init_from_module(klass, m):
    """
    Build a class passing the exported names from the given module as
    keyword arguments to its __init__ function.
    """
    params, args_name, kw_name, defaults = inspect.getargspec(klass.__init__)

    exports = set(getattr(m, '__all__', (name for name in m.__dict__ if not name.startswith('_'))))

    kw = {}

    # skip initial "self" argument
    for name in params[1:]:
        if name in exports:
            kw[name] = getattr(m, name)
    
    return klass(**kw)
    

def flatten(iter):
    """
    Turns an iterable of iterables of elements into a flat list of
    elements
    """
    return [x for x in chain(*[y for y in iter])]

class AutoRepr(object):
    """
    
    class X(AutoRepr):
        def __init__(self, name):
            self.name
        def
    """
    def __repr__(self):
        f = getattr(self.__class__, '__getnewargs__', None
                    ) or getattr(self.__class__, '__getinitargs__', None)
        if f:
            return self.__class__.__name__ + '(' + ', '.join(repr(x) for x in f(self)) + ')' 
        else:
            return object.__repr__(self)
    
    
if __name__ == '__main__':
    class X(AutoRepr):
        def __init__(self, name):
            self.name = name
        def __getinitargs__(self):
            return (self.name,)

    class Y(X):
        def __init__(self,num,name):
            X.__init__(self, name)

        def __new__(cls, num, name):
            ret = X.__new__(cls)
            ret.num = num
            return ret

        def __getnewargs__(self):
            return (self.num, self.name)

    assert repr(X('foo')) == "X('foo')"
    assert repr(Y(3, 'foo')) == "Y(3, 'foo')"
