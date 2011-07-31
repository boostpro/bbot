from master import BuildMaster
from bbot.util.quiet_process import check_call
from os.path import join as pjoin, dirname as pdir
from bbot.test.util import load_template
from bbot.util.path import Path

trivial_config_py_template = load_template('trivial-config.py')

class MasterTester(object):
    master = None

    def setUp(self):
        self.master = BuildMaster(self.gen_config)

    def test_checkconfig_in_src_dir(self):
        self.master.check_cmd(['checkconfig'], cwd=self.master.src_dir)

    def test_checkconfig_in_bot_dir(self):
        self.master.check_cmd(['checkconfig'])

    def test_life_cycle(self):
        self.master.check_cmd(['create-master'])
        self.master.check_cmd(['start'])
        self.master.check_cmd(['reconfig'])
        self.master.check_cmd(['stop'])


class trivial_config_tests(MasterTester):
    def gen_config(self, where):
        """
        Append some additional imports to the minimal config.py to
        test that the full module is available
        """
        open(where/'config.py', 'w').write(
            trivial_config_py_template + 
"""
import %(name)s.foo
import %(name)s
""" % dict(name=where.name))
        open(where/'foo.py', 'w')

    
class legacy_config_tests(MasterTester):
    def gen_config(self, where):
        config = Path(__file__).folder/'legacy_test_config.py'
        config.copy(where/'config.py')
    
