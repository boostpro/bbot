from buildbot.buildslave import BuildSlave
from memoize import memoize
from collections import Iterable
from platform import Platform

class Slave(BuildSlave):
    """
    A BuildSlave that can be initialized with a password after
    its initial construction.
    """
    def __init__(self, name, password=None, features={}, *args, **kw):
        """
        @type  name: string
        @param name: name given to BuildSlave

        @type  password: string or None
        @param password: buildslave password

        @type  features: dict mapping strings to strings or lists of strings
        @param features: Properties of this slave

        Additional arguments are passed on to the BuildSlave we construct
        """
        self.__name = name
        self.__password = password
        self.__args = args
        self.__kw = kw
        self.__features = features

    @property
    def features(self):
        return self.__features

    def prepare(self, passwords):
        BuildSlave.__init__(
            self,
            self.__name,
            self.__password or passwords[self.__name],
            *self.__args, **self.__kw)

    def platforms(self, relevant_features):
        """
        For a given sorted tuple of features, return a sequence of all
        platform tuples consisting of just those features that are
        supported by this slave.

        >>> s = Slave('foo', None, features=dict( a=(1, 2, 3), b=4, c=(5,6) ))
        >>> s.platforms(('a',))
        [Platform({'a': 1}), Platform({'a': 2}), Platform({'a': 3})]
        >>> s.platforms(('b',))
        [Platform({'b': 4})]
        >>> s.platforms(('a','b'))
        [Platform({'a': 1, 'b': 4}), Platform({'a': 2, 'b': 4}), Platform({'a': 3, 'b': 4})]
        >>> s.platforms(('a', 'c'))
        [Platform({'a': 1, 'c': 5}), Platform({'a': 1, 'c': 6}), Platform({'a': 2, 'c': 5}), Platform({'a': 2, 'c': 6}), Platform({'a': 3, 'c': 5}), Platform({'a': 3, 'c': 6})]
        >>> s.platforms(('d'))
        []
        """
        return [ Platform(x) for x in self.__platforms(relevant_features) ]

    def __platforms(self, relevant_features):
        i = iter(relevant_features)
        try:
            f = i.next()
        except StopIteration:
            return [()]

        vs = self.__features.get(f, ())
        if isinstance(vs, (str,unicode)) or not isinstance(vs, Iterable):
            vs = (vs,)

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
