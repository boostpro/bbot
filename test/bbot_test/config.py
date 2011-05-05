from bbot_test import bbot
from bbot_test.bbot.repository import GitHub
from bbot_test.bbot.project import Project
from bbot_test.bbot.slave import Slave
from bbot_test.bbot.procedures import BuildProcedure

BuildmasterConfig = bbot.master(
    title = 'bbot-test-site', 
    buildbotURL = 'http://buildbot.net', 


    slaves = [
        Slave('slave1', 'password1', features=dict(os='OS1', cc=['g++', 'vc8'])),
        Slave('slave2', 'password2', features=dict(os='OS2', cc=['intel', 'clang']))
        ], 

    projects = [
        Project('project1',
                repositories=[GitHub('boostpro/bbot')],
                include_features = ['cc'],
                build_procedures=[ BuildProcedure('build') ]
                ),
        Project('project2',
                repositories=[GitHub('boostpro/bbot')],
                include_features = ['os', 'cc'],
                build_procedures=[ 
                    BuildProcedure('build'), BuildProcedure('test')]
                ),
        ]
)

assert len(BuildmasterConfig['builders']) == 12
