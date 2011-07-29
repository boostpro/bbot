from master import BuildMaster
from subprocess import check_call

class checkconfig_test(BuildMaster):
    cmd = ['buildbot', 'checkconfig']

    def test_in_src_dir(self):
        check_call(self.cmd, cwd=self.src_dir, env = self.environ)

    def test_in_bot_dir(self):
        check_call(self.cmd, cwd=self.bot_dir, env = self.environ)

    def gen_config_py(self):
        """
        Append some additional imports to the minimal config.py to
        test that the full module is available
        """
        open(self.src_dir/'foo.py', 'w')
        return super(checkconfig_test,self).gen_config_py() + """
import %(name)s.foo
import %(name)s
""" % dict(name=self.name)
        
