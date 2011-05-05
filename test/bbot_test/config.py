from bbot_test import bbot
from bbot_test.bbot.repository import GitHub
from bbot_test.bbot.project import Project
from bbot_test.bbot.slave import Slave
from bbot_test.bbot.procedures import BuildProcedure

BuildmasterConfig = bbot.master(
    title = 'bbot-test-site', 
    buildbotURL = 'http://buildbot.net', 


    slaves = [
        Slave('slave1', 'password1', properties=dict(os='OS1', cc=['g++', 'vc8'])),
        Slave('slave2', 'password2', properties=dict(os='OS2', cc=['intel', 'clang']))
        ], 

    projects = [
        Project('project1',
                repositories=[GitHub('boostpro/bbot')],
                include_properties = ['cc'],
                build_procedures=[ BuildProcedure('build') ]
                ),
        Project('project2',
                repositories=[GitHub('boostpro/bbot')],
                include_properties = ['os', 'cc'],
                build_procedures=[ 
                    BuildProcedure('build'), BuildProcedure('test')]
                ),
        ]
)
