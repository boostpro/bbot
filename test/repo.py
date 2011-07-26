import tempfile
import shutil
import subprocess
import os
import path

class TempDir(object):
    path = None
    def __init__(self, *args, **kw):
        '''
        >>> d = TempDir()
        >>> os.path.isdir(d.path)
        True
        '''
        self.path = path.Path(tempfile.mkdtemp(*args, **kw))

    def __str__(self):
        return self.path
        
    def __del__(self):
        '''
        >>> d = TempDir()
        >>> p = d.path
        >>> f = p / 'foo'
        >>> _ = open(f, 'w')
        >>> os.path.exists(f)
        True
        >>> del d
        >>> os.path.exists(p)
        False
        '''
        if self.path:
            shutil.rmtree(self.path, ignore_errors=True)

class LocalGit(TempDir):
    def __init__(self, *args, **kw):
        '''
        >>> r = LocalGit()
        >>> subprocess.call(['git','status'], cwd=r.path) or None
        '''
        super(LocalGit, self).__init__(*args, **kw)
        subprocess.check_call(['git','init'], cwd=self.path)

    def add(self, relpath='.'):
        '''
        >>> from subprocess import *
        >>> r = LocalGit()
        >>> open(r.path/'README','w').close()
        >>> r.add('README')
        >>> rev = Popen(['git','rev-parse', 'HEAD'], stdout=PIPE, stderr=None, cwd=r.path).stdout.read()
        >>> check_call(['git','commit', '-m', 'comment'], cwd=r.path) or None
        >>> rev == Popen(['git','rev-parse', 'HEAD'], stdout=PIPE, cwd=r.path).stdout.read()
        False
        '''
        subprocess.check_call(['git','add', relpath], cwd=self.path)
        
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()
