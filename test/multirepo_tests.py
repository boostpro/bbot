import find_bbot, bbot
from master import BuildMaster
from slave import BuildSlave
from util import load_template
from bbot.util.repo import LocalGit

init_py = '__init__.py'
config_template = load_template('multirepo_config.py')

class multirepo_test(object):
    

    def setUp(self):
        self.local_repos = []
        self.remote_repos = []

        for i in range(2):
            r = LocalGit(bare=True)
            r.install_post_receive_hook()
            self.remote_repos.append(r)
            l = LocalGit(clone=r)
            open(l/init_py, 'w')
            l.add(init_py)
            l.commit()
            self.local_repos.append(l)
            
        self.master = BuildMaster(config_fn = self.gen_config)
        self.master.bot_dir.preserve()
        self.master.create_master()
        self.master.start()
        self.slave = BuildSlave()
        self.slave.bot_dir.preserve()

    def gen_config(self, directory):
        open(directory/'config.py', 'w').write(
            config_template % dict(
                repo0=self.local_repos[0],
                repo1=self.local_repos[1]))

    def test(self):
        repo = self.local_repos[0]
        open(repo/init_py, 'w').write('invalid python\n')
        repo.add(init_py)
        repo.commit()

        open(repo/init_py, 'w').write('# valid python\n')
        repo.add(init_py)
        repo.commit()

        
