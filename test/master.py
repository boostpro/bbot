import find_bbot
import bbot
import bbot.util.quiet_process as quietly
from bbot.util.tempdir import TempDir
from util import load_template
from bot import Bot

import os, sys, shutil
from os.path import dirname as pdir


def _link_or_copy(src, dst):
    """
    Make a symbolic link pointing at src from dst, but if that's not
    supported (e.g. on Windows XP), copy the file from src to dst.
    """
    try:
        os.symlink(src, dst)
    except:
        shutil.copyfile(src, dst)

class BuildMaster(Bot):
    """
    Represents a test of a BuildMaster installation
    """

    #
    # constants
    #
    master_cfg_template = load_template('master.cfg')

    environ = dict(
        os.environ.items()
        + [('PYTHONPATH',pdir(pdir(bbot.__file__)))])

    executable = 'buildbot'

    #
    # instance attributes
    #
    name = None
    """Name of the directory where the configuration sourcec lives"""

    bot_dir = None
    """Path to the directory where "buildbot create-master" gets run"""

    src_dir = None
    """Path to the directory containing the configuration source files"""

    def __init__(self, config_fn, name = 'buildmaster'):
        super(BuildMaster,self).__init__()
        self.name = name
        
        # Create a submodule
        self.src_dir = self.bot_dir / self.name
        os.mkdir(self.src_dir)
        open(self.src_dir/'__init__.py', 'w')


        # Create the master.cfg file
        master_cfg = self.src_dir/'master.cfg'
        open(master_cfg, 'w').write(
            self.master_cfg_template % dict(name=self.name))

        # Add a link to master.cfg in the bot directory
        _link_or_copy(master_cfg, self.bot_dir/'master.cfg')

        # Generate config.py
        config_fn(self.src_dir)

    def gen_config_py(self):
        """
        Return a string representing the contents of the buildmaster's
        config.py file.  Override this method if you want to test a
        nontrivial configuration.
        """
        return self.trivial_config_py_template % dict(name=self.name)

    def check_cmd(self, *popenargs, **kwargs):
        cmd = kwargs.pop('args', None)
        if cmd is None:
            cmd = popenargs[0]
            popenargs = popenargs[1:]
        cwd = kwargs.pop('cwd', self.bot_dir)

        quietly.check_call(*popenargs, args=['buildbot']+cmd, env = self.environ, cwd=cwd, **kwargs)

    def create_master(self):
        self.check_cmd(['create-master', '-r'])


