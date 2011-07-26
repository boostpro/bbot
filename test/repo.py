import tempdir
import quiet_process

class LocalGit(tempdir.TempDir):
    def __init__(self, *args, **kw):
        '''
        >>> r = LocalGit()
        >>> quiet_process.call(['git','status'], cwd=r.path)
        0
        '''
        super(LocalGit, self).__init__(*args, **kw)
        quiet_process.check_call(['git','init'], cwd=self.path)

    def add(self, relpath='.'):
        '''
        >>> from quiet_process import *
        >>> r = LocalGit()
        >>> open(r.path/'README','w').close()
        >>> r.add('README')
        >>> call(['git','rev-parse', 'HEAD'], cwd=r.path) == 0
        False
        >>> check_call(['git','commit', '-m', 'comment'], cwd=r.path)
        0
        >>> check_call(['git','rev-parse', 'HEAD'], cwd=r.path)
        0
        '''
        quiet_process.check_call(['git','add', relpath], cwd=self.path)
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
