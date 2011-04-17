config = {}

def master(
    name,
    bot_url,
    slaves,
    projects,
    name_url = None,
    slavePortnum = 9989,
    change_source = None
    ):

    # In case we're being reloaded
    config.clear()
    c = config

    ####### BUILDSLAVES

    # The 'slaves' list defines the set of recognized buildslaves. Each
    # element is a BuildSlave object, specifying a unique slave name and
    # password.  The same slave name and password must be configured on
    # the slave.

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
    from buildbot.changes.pb import PBChangeSource
    c['change_source'] = change_source or PBChangeSource()


    ####### SCHEDULERS

    from itertools import chain
    def flatten(iter):
        return [x for x in chain(*[y for y in iter])]

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
    from itertools import repeat

    c['status'] = flatten([s1(p1) for s1 in p1.status] for p1 in projects)

    ####### PROJECT IDENTITY

    # the 'projectName' string will be used to describe the project that this
    # buildbot is working on. For example, it is used as the title of the
    # waterfall HTML page. The 'projectURL' string will be used to provide a link
    # from buildbot HTML pages to your project's home page.

    c['projectName'] = name
    c['projectURL'] = name_url or bot_url

    # the 'buildbotURL' string should point to the location where the buildbot's
    # internal web server (usually the html.WebStatus page) is visible. This
    # typically uses the port number set in the Waterfall 'status' entry, but
    # with an externally-visible host name which the buildbot cannot figure out
    # without some help.

    c['buildbotURL'] = bot_url

    ####### DB URL

    # This specifies what database buildbot uses to store change and scheduler
    # state.  You can leave this at its default for all but the largest
    # installations.
    c['db_url'] = "sqlite:///state.sqlite"

    return c
