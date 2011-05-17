from buildbot.process import factory

class BuildProcedure(factory.BuildFactory):
    """
    >>> { BuildProcedure('a') : 1 }.get(BuildProcedure('b'))
    >>> 
    """
    compare_attrs = factory.BuildFactory.compare_attrs + ['name']

    def __init__(self, name):
        factory.BuildFactory.__init__(self)
        self.name = name

    def step(self, s):
        self.addStep(s)
        return self
    
    def addSteps(self, *steps_):
        for s in steps_:
            self.addStep(s)
        return self

    def __repr__(self):
        return self.__class__.__name__ + '(' + repr(self.name) + ')' 

if __name__ == '__main__':
    import doctest
    doctest.testmod()
