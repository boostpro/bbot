from master import BuildMaster
from bbot.util.quiet_process import check_call

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


class non_running_test(TrivialMaster):
    cmd = ['buildbot', 'checkconfig']

    def test_checkconfig_in_src_dir(self):
        self.check_cmd(['checkconfig'], cwd=self.src_dir)

    def test_checkconfig_in_bot_dir(self):
        self.check_cmd(['checkconfig'])

    def test_create_master(self):
        self.check_cmd(['create-master'])

class RunningMaster(BuildMaster):
    def setUp(self):
        super(RunningMaster,self).setUp()
        self.check_cmd(['create-master'])
        self.check_cmd(['start'])

    def tearDown(self):
        self.check_cmd(['stop'])
        super(RunningMaster,self).tearDown()

class trivial_run_test(TrivialMaster, RunningMaster):
    def test_reconfig(self):
        self.check_cmd(['reconfig'])
    def test_stop(self):
        self.check_cmd(['stop'])
