class Platform(tuple):
    """
    >>> a = Platform({'os':'linux', 'cc':'gcc'})
    >>> a
    Platform((('cc', 'gcc'), ('os', 'linux')))
    >>> print a
    gcc-linux
    >>> x = {}
    >>> b = Platform({'os':'linux', 'cc':'gcc'})
    >>> x[a] = 1
    >>> x[b]
    1
    >>> x.get(Platform({'os':'win', 'cc':'gcc'}))
    >>> 
    """
    def __new__(cls, rhs):
        if isinstance(rhs, dict):
            rhs = rhs.iteritems()
        return tuple.__new__(cls, sorted(rhs))

    def __str__(self):
        return '-'.join(str(x[1]) for x in self)

    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(tuple(self)) + ')'

if __name__ == "__main__":
    import doctest
    doctest.testmod()


