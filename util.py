import inspect, os, sys
from itertools import chain

def _import(module_name):
    __import__(module_name)
    return sys.modules[module_name]

def load_submodules(parent_module_name):
    """
    import and return a list of all submodules of the named module
    """
    print 'parent_module_name=', parent_module_name
    parent = _import(parent_module_name)
    print 'parent=', parent
    pdir = os.path.dirname(parent.__file__)
    print 'pdir=', pdir

    ret = []

    for x in os.listdir(pdir):
        submodule_name = None
        if not os.path.isdir(os.path.join(pdir, x)) and x.endswith('.py') and x != '__init__.py':
            submodule_name = os.path.splitext(x)[0]
        elif os.path.exists(os.path.join(pdir, x, '__init__.py')):
            submodule_name = x
        else:
            continue
        
        print 'submodule_name=', submodule_name
        print 'loading:', parent_module_name+'.'+submodule_name
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
