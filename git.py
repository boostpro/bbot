import re
from buildbot.steps.source import Git

from urlparse import urlsplit

git_ext_pattern = re.compile(r'\.git$')

# Pattern for matching git's special URIs
_url_pattern = re.compile(
    r'''^
     # handle any known schemes not handled by urlparse
     (?:(?P<scheme>git)://)?
     (?P<netloc>
          (?P<userpassat>[^/@]+@)?
          (?P<hostname>[-.a-zA-Z0-9]+))

     # if we found a known scheme, expect a slash. Otherwise (for
     # ssh), a colon.
     (?(scheme)/|:)

     # Looking for a non-slash here ensures we don't treat, e.g.,
     # 'http' as a netloc
     (?P<relpath>[^/].*)
     $'''
    , re.VERBOSE)

def split_url(url):
    """
    Break a git repository url into a tuple:

      (scheme, hostname, path, userpass), 

    where:

    - scheme is a url scheme such as 'http'
    - hostname is the name of the server
    - path is the path on that server
    - userpass is of the form '', '<username>', or 'username:password'
    
    >>> split_url('git@github.com:boostpro/bbot.git')
    ('ssh', 'github.com', '/boostpro/bbot', 'git')
    >>> split_url('http://github.com/boostpro/bbot')
    ('http', 'github.com', '/boostpro/bbot', '')
    >>> split_url('git://github.com/boostpro/bbot.git')
    ('git', 'github.com', '/boostpro/bbot', '')
    """
    
    url_sans_ext = git_ext_pattern.sub('', url)
    git_url = _url_pattern.match(url_sans_ext)
    if git_url:
        parts = (
            git_url.group('scheme') or 'ssh',
            git_url.group('netloc'),            
            '/' + git_url.group('relpath'), '', '')
    else:
        parts = urlsplit(url_sans_ext, scheme='file')

    (scheme, netloc, path, query, fragment) = parts
    
    # break netloc into user and host
    userpass,host = ([''] + netloc.split('@'))[-2:]

    return scheme, host, path, userpass

def probably_same_repo(url1, url2):
    """
    return True iff url1 and url2 probably refer to the same Git repository.

    See the multiple ways of referring to a repository provided by
    GitHub for the convention implemented here.

    Of course it's always possible for a given server to violate these
    conventions, but that would be perverse.

    >>> probably_same_repo('/foo/bar/baz', 'file:///foo/bar/baz')
    True
    >>> probably_same_repo('/foo/bar', 'file:///foo/bar/baz')
    False
    >>> probably_same_repo(
    ...   'git@github.com:boostpro/bbot.git'
    ... , 'http://github.com/boostpro/bbot')
    True
    >>> probably_same_repo(
    ...    'git://github.com/boostpro/bbot.git', 
    ...    'http://github.com/boostpro/bbot')
    True
    """
    return split_url(url1)[1:-1] == split_url(url2)[1:-1]

class SourceStep(Git):
    def repo_changed(self):
        return probably_same_repo(self.build.getSourceStamp().repository, self.repourl)

    def startVC(self, branch, revision, patch):
        if not self.repo_changed():
            branch,revision,patch = self.branch, None, None
        return Git.startVC(self, branch, revision, patch)

    def commandComplete(self, cmd):
        if self.repo_changed():
            # This is where the got_revision property gets set in the
            # buildbot Source step.  Only capture that if we're
            # working on the same repository.
            Git.commandComplete(self, cmd)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
