import os, sys, shutil
from os.path import dirname as pdir

_bbot_parent_dir = pdir(pdir(pdir(__file__)))
if _bbot_parent_dir not in sys.path:
    sys.path.insert(0, _bbot_parent_dir)

import bbot
from bbot.util.tempdir import TempDir

def _link_or_copy(src, dst):
    """
    Make a symbolic link pointing at src from dst, but if that's not
    supported (e.g. on Windows XP), copy the file from src to dst.
    """
    try:
        os.symlink(src, dst)
    except:
        shutil.copyfile(src, dst)

class BuildMaster(object):
    """
    Represents a BuildMaster installation
    """

    def _load_template(name):
        return open(os.path.join(pdir(__file__),name+'.template')).read()

    master_cfg_template = _load_template('master.cfg')
    trivial_config_py_template = _load_template('trivial-config.py')

    environ = dict(
        os.environ.items()
        + [('PYTHONPATH',pdir(pdir(bbot.__file__)))])

    name = None

    bot_dir = None
    """Path to the directory where "buildbot create-master" gets run"""

    src_dir = None
    """Path to the directory containing the configuration source files"""

    def __init__(self, name = 'buildmaster'):
        self.name = name

    def setUp(self):
        """
        Prepare a temporary directory containing all the basics
        """
        self.bot_dir = TempDir()

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
        open(self.src_dir/'config.py', 'w').write(
            self.gen_config_py())

    def tearDown(self):
        """
        Make sure the temporary directory is cleaned up.
        """
        del self.bot_dir

    def gen_config_py(self):
        """
        Return a string representing the contents of the buildmaster's
        config.py file.  Override this method if you want to test a
        nontrivial configuration.
        """
        return self.trivial_config_py_template % dict(name=self.name)
