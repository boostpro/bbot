from procedures import BuildProcedure
from buildbot.steps.source import Git
from buildbot.steps.shell import Test, SetProperty
from buildbot.steps.slave import SetPropertiesFromEnv
from buildbot.process.properties import WithProperties

def Emacs():
    return WithProperties(
        '%(EMACS)s'
        , EMACS=lambda build: build.getProperties().getProperty('EMACS','emacs')
        )

def EmacsTest(*args, **kw):
    return Test(
        command=[Emacs(), '--no-splash', '--debug-init'] + (
            list(args)
            + reduce(lambda r, kv: r+['--'+kv[0],kv[1]], kw.items(), [])),
        env = { 'HOME': WithProperties('%(FakeHome)s') },
        timeout = kw.get('timeout', 40),
        logfiles = dict(testlog=dict(filename='test.log'))
        )

class GitHubElisp(BuildProcedure):
    def __init__(self, repo, *testnames):
        BuildProcedure.__init__(self, 'elisp')
        self.addSteps(
            Git(repourl='git://github.com/%s.git' % repo),
            SetPropertiesFromEnv(variables=['EMACS']),
            SetProperty(
                command=[Emacs(), '--batch', '--eval',
                         '(princ (make-temp-file "home" t ".bbot"))'],
                extract_fn=lambda rc, stdout, stderr: dict(FakeHome=stdout)
                ))

        for t in testnames or ['test/test']:
            self.addStep(EmacsTest(load= t+'.el'))


