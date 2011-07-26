import tempfile
import shutil
import path
import os

class TempDir(path.Path):
    def __new__(cls, *args, **kw):
        '''
        >>> d = TempDir()
        >>> os.path.isdir(d)
        True
        '''
        d = tempfile.mkdtemp(*args, **kw)
        try:
            return super(TempDir,cls).__new__(cls, d)
        except:
            shutil.rmtree(d, ignore_errors=True)
            raise

    @property
    def path(self):
        '''
        >>> d = TempDir()
        >>> d.path == d
        True
        '''
        return path.Path(self)
            
    def __del__(self):
        '''
        >>> d = TempDir()
        >>> f = d / 'foo'
        >>> _ = open(f, 'w')
        >>> os.path.exists(f)
        True
        >>> p = str(d)
        >>> del d
        >>> os.path.exists(p)
        False
        '''
        if self.path:
            shutil.rmtree(self.path, ignore_errors=True)

if __name__ == '__main__':
    import doctest
    import os # used in tests
    doctest.testmod()
