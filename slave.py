from buildbot.buildslave import BuildSlave
from memoize import memoize
from collections import Iterable
from platform import Platform

class Slave(BuildSlave):
    """
    """
    def __init__(self, name, password=None, properties={}, *args, **kw):
        self.__name = name
        self.__password = password
        self.__args = args
        self.__kw = kw
        self.__properties = properties
    
    def prepare(self, passwords):
        BuildSlave.__init__(
            self,
            self.__name, 
            self.__password or passwords[self.__name], 
            properties=self.__properties, 
            *self.__args, **self.__kw)
    
    def platforms(self, features):
        """
        For a given sorted tuple of features, return a sequence of all
        platform tuples consisting of just those features that are
        supported by this slave.

        >>> s = Slave('foo', None, properties=dict( As=(1, 2, 3), B=4, Cs=(5,6) ))
        >>> s.platforms(('A',))
        [Platform((('A', 1),)), Platform((('A', 2),)), Platform((('A', 3),))]
        >>> s.platforms(('B',))
        [Platform((('B', 4),))]
        >>> s.platforms(('A','B'))
        [Platform((('A', 1), ('B', 4))), Platform((('A', 2), ('B', 4))), Platform((('A', 3), ('B', 4)))]
        >>> s.platforms(('A', 'C'))
        [Platform((('A', 1), ('C', 5))), Platform((('A', 1), ('C', 6))), Platform((('A', 2), ('C', 5))), Platform((('A', 2), ('C', 6))), Platform((('A', 3), ('C', 5))), Platform((('A', 3), ('C', 6)))]
        >>> s.platforms(('d'))
        []
        """
        return [ Platform(x) for x in self.__platforms(features) ]

    def __platforms(self, features):
        i = iter(features)
        try:
            f = i.next()
        except StopIteration:
            return [()]

        v = self.__properties.get(f)
        if v:
            vs = (v,)
        else:
            vs = self.__properties.get(f+'s', ())
        
        tails = self.platforms(i)

        r = []
        for v in vs:
            property = (f,v)
            for t in tails:
                r.append( (property,) + t )

        return r

if __name__ == "__main__":
    import doctest
    doctest.testmod()
