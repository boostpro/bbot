import re

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

    See the multiple ways of 

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

if __name__ == '__main__':
    import doctest
    doctest.testmod()
