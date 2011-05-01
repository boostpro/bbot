class Slave(object):
    def __init__(self, name, password=None, *args, **kw):
        self.name = name
        self.password = password
        self.args = args
        self.kw = kw
