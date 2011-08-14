import find_bbot, bbot
from master import BuildMaster
from slave import BuildSlave
from util import load_template
from bbot.util.repo import LocalGit
from monitor import Monitor

init_py = '__init__.py'
config_template = load_template('multirepo_config.py')

class multirepo_test(object):
    
    def setUp(self):
        self.monitor = Monitor()

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
            
        print 'creating master...'
        self.master = BuildMaster(config_fn = self.gen_config)
        self.master.bot_dir.preserve()
        self.master.create_master()
        print 'starting master in', self.master.bot_dir, '...'
        self.master.start()
        print 'creating slave...'
        self.slave = BuildSlave()
        print 'starting slave...'
        self.slave.bot_dir.preserve()
        print 'setUp complete.'

    def tearDown(self):
        self.master.stop()
        self.slave.stop()
        del self.monitor

    def gen_config(self, directory):
        open(directory/'config.py', 'w').write(
            config_template % dict(
                repo0=self.remote_repos[0],
                repo1=self.remote_repos[1]))

    def test(self):
        print 'starting test...'
        repo = self.local_repos[0]
        open(repo/init_py, 'w').write('invalid python\n')
        repo.add(init_py)
        repo.commit()
        print 'commit #1 to', repo
        repo.push()

        open(repo/init_py, 'w').write('# valid python\n')
        repo.add(init_py)
        repo.commit()
        print 'commit #2 to', repo
        repo.push()
        # self.master.stop()
        for m in self.monitor.messages():
            print '<== ', m['event'] # , 8*' ', m['payload']
