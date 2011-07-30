import os
if os.name == 'nt':
    from subprocess import list2cmdline

    def quote(arg):
        return list2cmdline([arg])[0]
else:
    import re
    _quote_pos = re.compile('(?=[^-0-9a-zA-Z_./\n])')

    def quote(arg):
        r"""
        >>> quote('\t')
        '\\\t'
        >>> quote('foo bar')
        'foo\\ bar'
        """
        # This is the logic emacs uses
        if arg:
            return _quote_pos.sub('\\\\', arg).replace('\n',"'\n'")
        else:
            return "''"

    def list2cmdline(args):
        return ' '.join([ quote(a) for a in args ])
