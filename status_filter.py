from memoize import memoize

class PublicStatus(object):
    """
    A Buildbot status filter that limits reporting to public projects.
    """
    # This should be commented more but I'm about to rip it out in
    # favor of separate private and public buildbots
    def __init__(self, base):
        self.__base = base

    def __getattr__(self, attr):
        return getattr(self.__base, attr)

    def getChangeSources(self):
        return []

    def getChange(self, number):
        # TODO: Figure out how to filter out private changes for extra security
        return self.__base.getChange(number)

    def getSchedulers(self):
        # TODO: Figure out how to filter out private schedulers for extra security
        return self.__base.getSchedulers()

    def getBuilderNames(self, categories=None):
        return filter(self.is_public_builder_name, self.__base.getBuilderNames())

    @memoize
    def is_public_builder_name(self, name):
        return is_public_BuilderStatus(self.__base.getBuilder(name))

    @memoize
    def getBuilder(self, name):
        b = self.__base.getBuilder(name)
        if not is_public_BuilderStatus(b): 
            raise KeyError, 'No such public builder'
        return b

    def getSlaveNames(self):
        return filter(is_public_slave_name, self.__base.getSlaveNames())

    def getSlave(self, name):
        s = self.__base.getSlave(name)
        if not is_public_SlaveStatus(s): 
            raise KeyError, 'No such public slave'
        return s

    def getBuildSets(self):
        # TODO: Figure out how to filter out private build sets for extra security
        return self.__base.getBuildSets()

    def generateFinishedBuilds(self, builders=[], branches=[],
                               num_builds=None, finished_before=None,
                               max_search=200):
        if not builders:
            public_builders = self.getBuilderNames()
        else:
            public_builders = filter(self.is_public_builder_name, builders)

        return self.__base.generateFinishedBuilds(
            public_builders, branches, num_builds, finished_before, max_search)

from buildbot.status.web.waterfall import WaterfallStatusResource
from buildbot.status.web.console import ConsoleStatusResource

class FilteredChangeManager(object):
    def __init__(self, base, filter):
        self.__base = base
        self.__filter = filter or (lambda x:True)

    def __getattr__(self, attr):
        return getattr(self.__base, attr)
    
    def eventGenerator(self, branches=[], categories=[],
                            committers=[], minTime=0):
        for change in self.__base.eventGenerator(
            branches,categories,committers,minTime):
            from twisted.python import log
            if self.__filter(change):
                yield change


class ChangeFilteredMixin(object):
    def __init__(self, base_class, filter, *args, **kw):
        base_class.__init__(self, *args, **kw)
        self.__base_class = base_class
        self.__filter = filter

    def getChangeManager(self, request):
        return FilteredChangeManager(
            self.__base_class.getChangeManager(self,request), 
            self.__filter)

class FilteredWaterfall(ChangeFilteredMixin, WaterfallStatusResource):
    def __init__(self, change_filter, *args, **kw):
        ChangeFilteredMixin.__init__(
            self, WaterfallStatusResource, change_filter, *args, **kw)

class FilteredConsole(ChangeFilteredMixin, ConsoleStatusResource):
    def __init__(self, change_filter, *args, **kw):
        ChangeFilteredMixin.__init__(
            self, ConsoleStatusResource, change_filter, *args, **kw)

import repository
def public_changes(changes):
    repo_url = changes.asDict().get('repository')
    if repo_url:
        repo = repository.repositories.get(repo_url)
        if repo:
            return repo.properties.get('public')
    return False
            

from buildbot.status import html
class FilteredWebStatus(html.WebStatus):
    """A Buildbot web status that limits reporting to a subset of changes, builders, etc."""
    def __init__(self, categories, status_filter=None, change_filter=public_changes, *args, **kw):
        self.__status_filter = status_filter
        self.__change_filter = change_filter
        html.WebStatus.__init__(self, *args, **kw)

    def getStatus(self):
        return (self.__status_filter or (lambda x:x))(
            html.WebStatus.getStatus(self))

    def setupUsualPages(self, numbuilds, num_events, num_events_max):
        html.WebStatus.setupUsualPages(self, numbuilds, num_events, num_events_max)

        # Replace these with their filtered variants
        self.putChild(
            "waterfall", FilteredWaterfall(
                change_filter=self.__change_filter,
                num_events=num_events, num_events_max=num_events_max))

        # Not sure the console is working; it doesn't seem to show up.
        self.putChild("console", FilteredConsole(
                change_filter=self.__change_filter, orderByTime=self.orderConsoleByTime))

def is_public_SlaveStatus(s):
    return is_public_slave_name(s.getName())

@memoize
def is_public_slave_name(name):
    return (
        (s for s in config['slaves'] if s.slavename == name).next()).properties.getProperty('public')

@memoize
def is_public_BuilderStatus(builderStatus):
    return all(is_public_SlaveStatus(s) for s in builderStatus.getSlaves())

