import re, git
import buildbot.steps.source
from twisted.python import log

repositories = {}

class Repository(object):

    stepClass = None

    def __init__(self, url, properties=None):
        self.url = url
        self.properties = properties or {}
        repositories[url] = self

    def set_properties(self, include, exclude):
        for p in include:
            if p in self.properties:
                if not self.properties[p]:
                    raise ValueError, \
                        'property %s was already excluded from repository %s: %s' % (
                        p,self.url, self.properties)
            else:
                self.properties[p] = True

        for p in exclude:
            if p in self.properties:
                if self.properties[p]:
                    raise ValueError, \
                        'property %s was already included in repository %s: %s' % (
                        p,self.url, self.properties)
            else:
                self.properties[p] = False

    def match_url(self, url):
        """Used for change filtering; True iff url identifies the same repository."""
        return self.url == url

    def steps(self, *args, **kw):
        return [ self.stepClass(repourl = self.url, *args, **kw) ]


class GitStep(buildbot.steps.source.Git):
    def computeSourceRevision(self, changes):
        if changes:
            for c in list(changes).reversed():
                log.msg('checking repo match: %s/%s' % (c.repository, self.repourl))
                if git.probably_same_repo(c.repository, self.repourl):
                    log.msg('MATCHED')
                    return c.revision
        return None

class Git(Repository):
    """
    A repository whose steps use Git, but unlike BuildBot, *do*
    consider submodules by default.  Seriously, who wants to ignore
    submodules?
    """
    stepClass = GitStep

    def steps(self, *args, **kw):
        kw.setdefault('submodules', True)
        return super(Git,self).steps(*args, **kw)

    @property
    def name(self):
        """
        The name of the repository: the last element of the url, sans .git extension if any
        """
        return re.match('.*/(.*?)(?:.git)?$', self.url).group(1)

class GitHub(Git):
    protocols=dict(
        git='git://github.com/%s',
        http='http://github.com/%s',
        https='https://github.com/%s',
        ssh='git@github.com:%s',
        )

    def __init__(self, id, protocol='http'):
        
        super(GitHub,self).__init__(GitHub.protocols[protocol] % id)
        self.id = id
        self.protocol = protocol

    def __repr__(self):
        return self.__class__.__module__ + '.' \
            + self.__class__.__name__+repr((self.id,self.protocol))

    def match_url(self, url):
        return git.probably_same_repo(self.url,url)
