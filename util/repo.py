import tempdir
import quiet_process as quietly

def _nonempty_repo(add=True,commit=None):
    r = LocalGit()
    open(r.path/'README','w').close()
    if add:
        r.check_call(['add', 'README'])
    if commit or commit is None and add:
        r.check_call(['commit', '-m', 'Empty commit message'])
    return r

class LocalGit(tempdir.TempDir):
    def __init__(self, *args, **kw):
        '''
        >>> git = LocalGit()
        >>> quietly.check_call(['git','status'], cwd=git.path)
        '''
        super(LocalGit, self).__init__(*args, **kw)
        self.check_call(['init'])

    def rev_parse(self, rev='HEAD'):
        '''
        >>> import re
        >>> git = _nonempty_repo()
        >>> rev = git.rev_parse()
        >>> len(rev)
        40
        >>> assert re.match('[0-9a-f]{40}', rev)
        '''
        return quietly.check_output(['git','rev-parse', rev], cwd=self.path).strip()

    def add(self, relpath='.'):
        '''
        >>> git = _nonempty_repo(add=False)
        >>> git.add('README')
        >>> git.check_call(['commit', '-m', 'xx'])
        >>> git.check_call(['rev-parse', 'HEAD'])
        '''
        self.check_call(['add', relpath])

    def commit(self, msg='Empty commit message'):
        '''
        >>> git = _nonempty_repo(commit=False)
        >>> git.commit()
        >>> git.check_call(['rev-parse', 'HEAD'])
        '''
        self.check_call(['commit', '-m', msg])

    def check_call(self, *args, **kw):
        '''
        >>> LocalGit().check_call(['status'])
        >>> try: LocalGit().check_call(['not a real command'])
        ... except: pass
        '''
        return quietly.check_call( ['git']+args[0],
            *args[1:], **dict(kw, cwd=kw.get('cwd',self.path)))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
