from master import BuildMaster, RunningMaster
from bbot.util.quiet_process import check_call
from os.path import join as pjoin, dirname as pdir

class TrivialMaster(BuildMaster):
    def gen_config_py(self):
        """
        Append some additional imports to the minimal config.py to
        test that the full module is available
        """
        open(self.src_dir/'foo.py', 'w')
        return super(TrivialMaster,self).gen_config_py() + """
import %(name)s.foo
import %(name)s
""" % dict(name=self.name)

class checkconfig_and_create(BuildMaster):
    def test_checkconfig_in_src_dir(self):
        self.check_cmd(['checkconfig'], cwd=self.src_dir)

    def test_checkconfig_in_bot_dir(self):
        self.check_cmd(['checkconfig'])

    def test_create_master(self):
        self.check_cmd(['create-master'])

class reconfig_and_stop(RunningMaster):
    def test_reconfig(self):
        self.check_cmd(['reconfig'])
    def test_stop(self):
        self.check_cmd(['stop'])

class trivial_static_tests(TrivialMaster, checkconfig_and_create):
    pass
class trivial_running_tests(TrivialMaster, reconfig_and_stop):
    pass

class LegacyMaster(BuildMaster):
    def gen_config_py(self):
        return open(
            pjoin(pdir(__file__), 'legacy_test_config.py')).read()

class legacy_static_tests(LegacyMaster, checkconfig_and_create):
    pass
class legacy_running_tests(LegacyMaster, reconfig_and_stop):
    pass
