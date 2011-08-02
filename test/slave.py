from bot import Bot

class BuildSlave(Bot):
    executable = 'buildslave'

    def __init__(self, name='slave', passwd='password'):
        super(BuildSlave,self).__init__()
        self.check_cmd(
            ['create-slave', '-r', self.bot_dir, 'localhost', name, passwd])
        self.start()
