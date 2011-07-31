import quiet_process as quietly
import shell
from path import Path
import tempdir
import os

def _nonempty_repo(add=True,commit=None):
    r = LocalGit()
    open(r.path/'README','w').close()
    if add:
        r.check_call(['add', 'README'])
    if commit or commit is None and add:
        r.check_call(['commit', '-m', 'Empty commit message'])
    return r

class LocalGit(tempdir.TempDir):

    def __new__ (cls, bare=False, clone=None, *args, **kw):
        if bare:
            kw['suffix'] = '.git'
        return super(LocalGit, cls).__new__(cls, *args, **kw)

    def __init__(self, bare=False, clone=None, *args, **kw):
        '''
        >>> git = LocalGit()
        >>> quietly.check_call(['git','status'], cwd=git.path)
        >>> clone = LocalGit(clone=git)
        >>> quietly.check_call(['git','status'], cwd=clone.path)
        '''
        super(LocalGit, self).__init__(*args, **kw)
        options = bare and ['--bare'] or []
        if clone:
            self.check_call(['clone'] + options + [clone, self.name], cwd = self.folder)
        else:
            self.check_call(['init'] + options)

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
        >>> try: LocalGit().check_call(['expected failure'])
        ... except: pass
        '''
        return quietly.check_call( ['git']+args[0],
            *args[1:], **dict(kw, cwd=kw.get('cwd',self.path)))
    
    @property
    def dot_git(self):
        return self if self.endswith('.git') else self/'.git'

    def install_post_receive_hook(self, **kw):
        r'''
        >>> remote = LocalGit(bare=True)
        >>> remote.preserve()
        >>> hook = remote.install_post_receive_hook()
        >>> cont = open(hook).read()
        >>> open(hook, 'a').write('set -e\n' + cont + 'echo done > ' + shell.quote(remote/'done'))
        >>> local = _nonempty_repo()
        >>> local.check_call(['remote', 'add', 'origin', remote])
        >>> local.check_call(['push', 'origin', 'master:foo'], cwd=local)
        >>> assert (remote/'done').exists
        '''
        hookpath = self.dot_git/'hooks'/'post-receive'
        hook = open(hookpath, 'w')

        buildbot_src = Path(__file__).folder.folder/'external'/'buildbot'
        script = buildbot_src/'master'/'contrib'/'git_buildbot.py'
        kw['repository'] = kw.get('repository', self)

        cmd = [ script, '-v' ]
        for k,v in kw.items():
            cmd += [ '--' + k, v]

        hook.write(shell.list2cmdline(cmd) + ' || exit 1\n')
        hook.close()
        os.lchmod(hookpath, 0777)
        return hookpath

        
if __name__ == '__main__':
    import doctest
    doctest.testmod()

