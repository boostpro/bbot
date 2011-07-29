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
        check_call(self.cmd, cwd=self.src_dir, env = self.environ)

    def test_checkconfig_in_bot_dir(self):
        check_call(self.cmd, cwd=self.bot_dir, env = self.environ)

    def test_create_master(self):
        check_call(['buildbot', 'create-master'], cwd=self.bot_dir, env = self.environ)

class RunningMaster(BuildMaster):
    def setUp(self):
        super(RunningMaster,self).setUp()
        check_call(['buildbot', 'create-master'], cwd=self.bot_dir, env = self.environ)
        check_call(['buildbot', 'start'], cwd=self.bot_dir, env = self.environ)

    def tearDown(self):
        check_call(['buildbot', 'stop'], cwd=self.bot_dir, env = self.environ)
        super(RunningMaster,self).tearDown()

class trivial_run_test(TrivialMaster, RunningMaster):
    def test_reconfig(self):
        check_call(['buildbot', 'reconfig'], cwd=self.bot_dir, env = self.environ)
    def test_stop(self):
        check_call(['buildbot', 'stop'], cwd=self.bot_dir, env = self.environ)
