from twisted.trial import unittest
import os, sys

class Doctests(unittest.TestCase):
    def test_submodules(self):
        
        import inspect

        # put bbot in the path
        sys.path.append(
            reduce(
                lambda path,_:os.path.dirname(path), 
                range(4), 
                os.path.join(
                    os.getcwd(),
                    inspect.getfile(inspect.currentframe()))))

        import doctest
        import bbot
        doctest.testmod(bbot)

        from bbot.util import load_submodules
        for s in load_submodules('bbot', recurse=True):
            print 'testing', s.__name__
            doctest.testmod(s)
