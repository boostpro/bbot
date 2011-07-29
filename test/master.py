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

    master_cfg_template = """# -*- python -*-
# ex: set syntax=python:

# This file is boilerplate.
#
import os, sys, lazy_reload

lazy_reload.lazy_reload(%(name)r)

# When buildbot checkconfig is invoked from the root directory of the
# project (as opposed to its parent), we need to amend the path so
# this module can be found.
try:
    import %(name)s
except ImportError:
    sys.path[-1] = os.path.dirname(sys.path[-1])

# All the real work gets done in config.py
from %(name)s.config import *
"""

    trivial_config_py_template = """
import bbot

BuildmasterConfig = bbot.master(
    title = '%(name)s', 
    buildbotURL = 'http://trac.buildbot.net',
    slaves = [],
    projects = []
)
"""
    environ = dict(
        os.environ.items()
        + [('PYTHONPATH',pdir(pdir(bbot.__file__)))])

    name = None
    parent_dir = None
    cfg_dir = None

    def __init__(self, name = 'buildmaster'):
        self.name = name

    def setUp(self):
        self.parent_dir = TempDir()
        self.cfg_dir = self.parent_dir / self.name
        os.mkdir(self.cfg_dir)

        master_cfg = self.cfg_dir/'master.cfg'
        open(master_cfg, 'w').write(
            self.master_cfg_template % dict(name=self.name))
        
        _link_or_copy(master_cfg, self.parent_dir/'master.cfg')

        open(self.cfg_dir/'__init__.py', 'w')

        open(self.cfg_dir/'config.py', 'w').write(
            self.gen_config_py())
        
    def tearDown(self):
        del self.parent_dir

    def gen_config_py(self):
        """
        Return a string representing the contents of the buildmaster's
        config.py file.
        """
        return self.trivial_config_py_template % dict(name=self.name)
