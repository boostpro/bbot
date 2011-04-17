import functools
class memoize(object):
    """
    A decorator that adds memoization to any method, thereby avoiding
    recomputation of the value.
    """
    __memos = {}
    class __nothing: pass

    def __init__(self, fn):
        self.fn = fn

    def __method(self, target, *args):
        attrname = '_memoize__' + self.fn.__name__
        memos = getattr(target, attrname, {})
        if args in memos:
            return memos[args]
        elif not memos:
            setattr(target, attrname, memos)
        result = self.fn(target, *args)
        memos[args] = result
        return result
    
    def __call__(self, *args):
        key = (self.fn,)+args
        v = self.__memos.get(key,self.__nothing)
        if v is self.__nothing:
            v = self.__memos[key] = self.fn(*args)
        return v

    def __get__(self, obj, objtype):
        # Support instance methods.
        return functools.partial(self.__method, obj)

