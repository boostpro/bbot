from os.path import dirname as pdir, join as pjoin

def load_template(name):
    return open(pjoin(pdir(__file__), name+'.template')).read()
