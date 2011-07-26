from subprocess import Popen as _Popen, PIPE, STDOUT, call as _call, check_call as _check_call, CalledProcessError

def _quiet_args(kwargs):
    return dict(
        kwargs, 
        stdout=kwargs.get('stdout', PIPE), 
        stderr=kwargs.get('stderr', PIPE))

class Popen(_Popen):
    def __init__(self, *args, **kw):
        super(Popen,self).__init__(*args, **_quiet_args(kw))

def call(*args, **kw):
    return _call(*args, **_quiet_args(kw))

def check_call(*args, **kw):
    return _check_call(*args, **_quiet_args(kw))

try:
    from subprocess import check_output as _check_output
except:
    # lifted directly from Python 2.7 source
    def check_output(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = Popen(stdout=PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise CalledProcessError(retcode, cmd)
        return output
else:
    def check_output(*args, **kw):
        return _check_output(*args, **dict(kw, stderr=kw.get('stderr', PIPE)))
                           
