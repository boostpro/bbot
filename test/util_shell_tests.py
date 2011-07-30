import os, sys, tempfile

from bbot.util import shell

def check_quote(*args):
    # Write a python script that compares an expected list of
    # arguments to what was actually passed on the command line
    script = tempfile.NamedTemporaryFile(suffix='.py')
    script.write("""
import sys
expected = %r
for x,y in zip(expected, sys.argv[1:]):
    assert x == y, repr(x)+' was quoted as '+repr(y)
assert len(expected) == len(sys.argv[1:])
""" % list(args)
        )
    script.flush()

    # Build the command string
    command = shell.list2cmdline((sys.executable, script.name) + args)

    # Make sure it's not too long for windows shells
    assert len(command) < 256
    assert os.system(command) == 0
    
def known_problematic_quote_test():
    """
    Shell-quoting arguments containing backslashes
    """
    check_quote(r'\r')

def trivial_quote_test():
    """
    Shell-quoting some things with spaces in them
    """
    check_quote('foo bar', 'baz')

def random_quote_test():
    """
    Shell-quoting a bunch of random strings
    """
    for x in range(30):
        check_quote( *[a for a in [os.urandom(5) for b in range(10)] if '\0' not in a])
