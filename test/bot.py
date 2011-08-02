import find_bbot

import bbot.util.quiet_process as quietly
from bbot.util.tempdir import TempDir
import os

class Bot(object):
    executable = None
    environ = os.environ.copy()

    running = False
    """True iff the bot has been successfully started and not stopped since"""

    def __init__(self):
        self.bot_dir = TempDir()

    def __del__(self):
        if self.running:
            self.stop()
        
    def check_cmd(self, *popenargs, **kwargs):
        cmd = kwargs.pop('args', None)
        if cmd is None:
            cmd = popenargs[0]
            popenargs = popenargs[1:]
        cwd = kwargs.pop('cwd', self.bot_dir)

        quietly.check_call(*popenargs, args=[self.executable]+cmd, env = self.environ, cwd=cwd, **kwargs)
    
    def start(self):
        self.running = True
        self.check_cmd(['start'])

    def stop(self):
        self.check_cmd(['stop'])
        self.running = False
