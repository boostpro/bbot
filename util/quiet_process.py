from subprocess import Popen as _Popen, PIPE, STDOUT, call as _call, check_call as _check_call, CalledProcessError as _CalledProcessError
import sys

def _quiet_args(kwargs):
    return dict(
        kwargs,
        stdout=kwargs.get('stdout', PIPE),
        stderr=kwargs.get('stderr', PIPE))

class Popen(_Popen):
    def __init__(self, *args, **kw):
        super(Popen,self).__init__(*args, **_quiet_args(kw))

    def __del__(self):
        try:
            self.kill()
        except:
            pass
        super(Popen,self).__del__()

def call(*args, **kw):
    return _call(*args, **_quiet_args(kw))

class CalledProcessError(_CalledProcessError):
    def __init__(self, returncode, cmd, output=None, stderr=None):
        super(CalledProcessError,self).__init__(returncode, cmd, output)
        self.stderr = stderr
        self.stdout = output

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d" % (
            self.cmd, self.returncode) + '''
### stderr:
''' + (self.stderr if self.stderr else '') + '''
### stdout:
''' + (self.stdout if self.stdout else '')

def check_call(*popenargs, **kwargs):
    # intentionally don't return anything.  _check_call throws if the
    # result would be nonzero, so the return value is meaningless
    p = Popen(*popenargs, **kwargs)
    retcode = p.wait()

    if retcode != 0:
        cmd = kwargs.get("args") or popenargs[0]
        raise CalledProcessError(retcode, cmd, output = p.stdout.read(), stderr = p.stderr.read())

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

