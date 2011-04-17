from buildbot.status import html
from buildbot.status.web import authz
from status_filter import *

class StatusFactory(object):
    """
    A function object that creates Buildbot Status objects for Projects
    """
    def __init__(self, klass, *args, **kw):
        self.klass = klass
        self.args = args
        self.kw = kw

    def __call__(self, project):
        return self.klass(*self.args, categories=[project.name], **self.kw)

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

def GitHubWebStatus(project, authz=default_authz, *args, **kw):
    """Generates WebStatus specifically for github projects"""
    return WebStatus(*args, 
                      authz=authz,
                      order_console_by_time=True,
                      revlink='http://github.com/'+project+'/commit/%s',
                      change_hook_dialects={ 'github' : True },
                      **kw)


