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

    def step(self, *args, **kw):
        return self.stepClass(repourl = self.url, *args, **kw)


import buildbot.steps.source

class Git(Repository):
    """
    A repository whose steps use Git, but unlike BuildBot, *do*
    consider submodules by default.  Seriously, who wants to ignore
    submodules?
    """
    stepClass = buildbot.steps.source.Git

    def step(self, *args, **kw):
        kw.setdefault('submodules', True)
        return super(Git,self).step(*args, **kw)

class GitHub(Git):
    def __init__(self, id, protocol='https'):
        
        ## NOTE: do *not* add the .git suffix here; the repository
        ## that comes back from the GitHub service hook doesn't have
        ## it.  Unless they match no builds will be triggered!
        protocols=dict(
            git='git://github.com/%s',
            http='http://github.com/%s',
            https='https://github.com/%s',
            ssh='git@github.com:%s',
            )

        super(GitHub,self).__init__(protocols[protocol] % id)

