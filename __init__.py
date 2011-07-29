import os
from util import flatten
from buildbot.changes.pb import PBChangeSource
from lazy_reload import lazy_reload

def master(
    title,
    buildbotURL,
    slaves,
    projects,
    titleURL = None,
    slavePortnum = 9989,
    change_source = None,
    passwd_path = None,
    status = []
    ):


    # projects can be a module name whose submodules each describe a
    # project by exporting attributes
    if isinstance(projects, str):
        lazy_reload(projects)
        p = []
        from util import load_submodules
        import project
        for m in load_submodules(projects):
            p.append(project.from_module(m))
        projects = p

    c = {}

    ####### PASSWORDS

    # If you have chosen not to store passwords directly in the .cfg
    # file, you can provide the path to a passwords file that will be
    # parsed here.
    if passwd_path is None:
        passwd_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'passwd')

    passwords = None
    if os.path.isfile(passwd_path):
        passwords = dict(line.rstrip().split(':') for line in open(passwd_path))

    ####### BUILDSLAVES

    # The 'slaves' list defines the set of recognized buildslaves. Each
    # element is a BuildSlave object, specifying a unique slave name and
    # password.  The same slave name and password must be configured on
    # the slave.

    for s in slaves: s.prepare(passwords)
    c['slaves'] = slaves

    # 'slavePortnum' defines the TCP port to listen on for connections from slaves.
    # This must match the value configured into the buildslaves (with their
    # --master option)
    c['slavePortnum'] = slavePortnum

    ####### CHANGESOURCES

    # the 'change_source' setting tells the buildmaster how it should find out
    # about source code changes. Any class which implements IChangeSource can be
    # put here: there are several in buildbot/changes/*.py to choose from.

    # This is the one used for BoostPro git repo changes
    c['change_source'] = change_source or PBChangeSource()


    ####### SCHEDULERS

    for p in projects:
        p.select_slaves(c['slaves'])

    # Configure the Schedulers, which decide how to react to incoming changes.
    c['schedulers'] = flatten(p.schedulers for p in projects)

    ####### BUILDERS

    # The 'builders' list defines the Builders, which tell Buildbot how to perform a build:
    # what steps, and which slaves can execute them.  Note that any particular build will
    # only take place on one slave.

    c['builders'] = flatten(p.builders for p in projects)

    c['mergeRequests']=False

    ####### STATUS TARGETS

    # 'status' is a list of Status Targets. The results of each build will be
    # pushed to these targets. buildbot/status/*.py has a variety to choose from,
    # including web pages, email senders, and IRC bots.
    c['status'] = flatten([s1(p1) for s1 in p1.status] for p1 in projects) + status

    ####### PROJECT IDENTITY

    # the 'projectName' string will be used to describe the project that this
    # buildbot is working on. For example, it is used as the title of the
    # waterfall HTML page. The 'projectURL' string will be used to provide a link
    # from buildbot HTML pages to your project's home page.

    c['projectName'] = title
    c['projectURL'] = titleURL or buildbotURL

    # the 'buildbotURL' string should point to the location where the buildbot's
    # internal web server (usually the html.WebStatus page) is visible. This
    # typically uses the port number set in the Waterfall 'status' entry, but
    # with an externally-visible host name which the buildbot cannot figure out
    # without some help.

    c['buildbotURL'] = buildbotURL.rstrip('/') + '/'

    ####### DB URL

    # This specifies what database buildbot uses to store change and scheduler
    # state.  You can leave this at its default for all but the largest
    # installations.
    c['db_url'] = "sqlite:///state.sqlite"

    return c
