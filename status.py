from buildbot.status import html
from buildbot.status.web import authz
from status_filter import *
from twisted.python import log
import re

class StatusFactory(object):
    """
    A function object that creates Buildbot Status objects for Projects
    """
    def __init__(self, klass, *args, **kw):
        self.klass = klass
        self.args = args
        self.kw = kw

    def __call__(self, project=None):
        return self.klass(*self.args, categories=project and [project.name] or None, **self.kw)

default_authz=authz.Authz(
    gracefulShutdown = True,
    forceBuild = True,
    forceAllBuilds = True,
    pingBuilder = True,
    stopBuild = True,
    stopAllBuilds = True,
    cancelPendingBuild = True,
)

def WebStatus(authz=default_authz, order_console_by_time=True, *args, **kw):
    """Generates a StatusFactory for FilteredWebStatus"""
    return StatusFactory(FilteredWebStatus, *args, 
                         authz=authz,
                         order_console_by_time=order_console_by_time, **kw)

def IRC(*args, **kw):
    """Generates a StatusFactory for IRC"""
    from buildbot.status import words
    return StatusFactory(words.IRC, *args, **kw)

def MailNotifier(*args, **kw):
    """Generates a StatusFactory for MailNotifier"""
    from buildbot.status import mail
    return StatusFactory(mail.MailNotifier, *args, **kw)


_url_pat = re.compile(r'(?:git@|(?:https?|git)://(?:[^@]+@)?)github.com[:/](.*?)(?:\.git)?$')

def _revlink(sha, repo):
    """
    >>> _revlink('deadbeef', 'git@github.com:user/repo.git')
    'http://github.com/user/repo/commit/deadbeef'
    >>> _revlink('deadbeef', 'http://github.com/user/repo.git')
    'http://github.com/user/repo/commit/deadbeef'
    >>> _revlink('deadbeef', 'https://userid@github.com/user/repo.git')
    'http://github.com/user/repo/commit/deadbeef'
    >>> _revlink('deadbeef', 'git://github.com/boostpro/lazy_reload.git')
    'http://github.com/boostpro/lazy_reload/commit/deadbeef'
    >>> _revlink('deadbeef', 'git://github.com/boostpro/lazy_reload')
    'http://github.com/boostpro/lazy_reload/commit/deadbeef'
    >>> _revlink('deadbeef', 'https://github.com/ryppl/Boost.Defrag')
    'http://github.com/ryppl/Boost.Defrag/commit/deadbeef'
    """
    m = _url_pat.match(repo)
    if not m:
        log.msg('GitHubWebStatus: unparseable url %r' % repo)
        return 'unparseable:'+repo

    return 'http://github.com/'+m.group(1)+'/commit/' + sha

def GitHubWebStatus(authz=default_authz, *args, **kw):
    """Generates WebStatus specifically for github projects"""

    return WebStatus(*args, 
                      authz=authz,
                      order_console_by_time=True,
                      revlink=_revlink,
                      change_hook_dialects={ 'github' : True },
                      **kw)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
