import tempdir
import quiet_process as quietly

class LocalGit(tempdir.TempDir):
    def __init__(self, *args, **kw):
        '''
        >>> r = LocalGit()
        >>> quietly.call(['git','status'], cwd=r.path)
        0
        '''
        super(LocalGit, self).__init__(*args, **kw)
        self.check_call(['git','init'])

    def add(self, relpath='.'):
        '''
        >>> r = LocalGit()
        >>> open(r.path/'README','w').close()
        >>> r.add('README')
        >>> quietly.call(['git','rev-parse', 'HEAD'], cwd=r.path) == 0
        False
        >>> r.check_call(['git','commit', '-m', 'comment'])
        0
        >>> r.check_call(['git','rev-parse', 'HEAD'])
        0
        '''
        self.check_call(['git','add', relpath])
        
    def commit(self, msg='Empty commit message'):
        '''
        >>> r = LocalGit()
        >>> open(r.path/'README','w').close()
        >>> r.add('README')
        >>> quietly.call(['git','rev-parse', 'HEAD'], cwd=r.path) == 0
        False
        >>> r.commit()
        >>> r.check_call(['git','rev-parse', 'HEAD'])
        0
        '''
        self.check_call(['git','commit', '-m', msg])

    def check_call(self, *args, **kw):
        '''
        >>> LocalGit().check_call(['git', 'status'])
        0
        '''
        return quietly.check_call(
            *args, **dict(kw, cwd=kw.get('cwd',self.path)))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
