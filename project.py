from buildbot.scheduler import AnyBranchScheduler
from buildbot.schedulers.filter import ChangeFilter
from memoize import memoize, const_property
import util

class multimap(dict):
    """
    A lazy dict of lists (sort of like a C++ std::multimap).

    Accessing a key not already in the dict creates a corresponding
    element whose value is the empty list.
    """
    def __getitem__(self, key):
        return self.setdefault(key, [])

def slave_property_match(slave, include, exclude):
    """Returns true iff the slave has all properties in include and none in exclude"""
    return (all(slave.properties.getProperty(x) for x in include) and
            not any(slave.properties.getProperty(x) for x in exclude))

class Project(object):

    __all_slaves = None

    """
    A software project
    """
    def __init__(
        self, 
        name,                       # the project's name, a string
        repositories,               # a sequence of repository.Repository's
        build_procedures,           # a sequence of procedure.BuildProcedure's
        include_properties=[],      # a sequence of property names that all testing slaves must posses
        exclude_properties=[],      # a sequence of property names that testing slaves must not posses
        make_change_filter=None,    # a function called on this project to produce a suitable ChangeFilter
        status=[]                   # a sequence of status reporters for this project
    ):
        self.name = name
        self.repositories = repositories
        for repo in self.repositories:
            repo.set_properties(include_properties, exclude_properties)
        self.build_procedures = build_procedures
        self.include_properties = include_properties
        self.exclude_properties = exclude_properties
        self.status = status
        if make_change_filter:
            self.change_filter = make_change_filter(self)
        else:
            self.change_filter = self.default_change_filter()

    def __str__(self):
        return 'Project %s (slaves=%s)' % (self.name,self.slaves)

    def uses_slave(self, slave):
        """Predicate returning True iff the given slave is eligible for use by this Project"""
        return slave_property_match(slave, self.include_properties, self.exclude_properties)

    def select_slaves(self, slaves):
        """Given a list of all eligible slaves, select the ones on which this project will build"""
        self.__all_slaves = slaves

    def default_change_filter(self, *args, **kw):
        """The default change filter builds all changes in the given repositories"""
        return ChangeFilter(repository=[r.url for r in self.repositories], *args, **kw)

    @const_property
    def slaves(self):
        """A list of the slaves used by this project"""
        return [s for s in self.__all_slaves if self.uses_slave(s)]

    @const_property
    def platforms(self):
        """A dict mapping platforms to lists of slaves"""
        r = multimap()
        for s in self.slaves:
            for p in s.platforms(self.include_properties):
                r[p].append(s)
        return r

    @memoize
    def builder(self, platform, procedure):
        """Returns a builder for this project on the named platform using a given BuildProcedure"""
        id = self.name+'-'+str(platform)+'-'+procedure.name
        return dict(
            name=id,
            slavenames=[s.slavename for s in self.platforms[platform]],
            properties=dict(platform),
            category=self.name,
            builddir=id,
            factory=procedure)

    @const_property
    def builders(self):
        """A list of this project's builders"""
        return [
            self.builder(platform,procedure) 
            for platform in self.platforms 
            for procedure in self.build_procedures]

    @const_property
    def schedulers(self):
        """A list of this project's schedulers"""
        # We need a scheduler for each build procedure
        return [
            AnyBranchScheduler(
                name=self.name+'-'+procedure.name+'-scheduler', 
                change_filter=self.change_filter,
                treeStableTimer=30,
                builderNames=[
                    self.builder(platform,procedure)['name']
                    for platform in self.platforms
                    ])
            for procedure in self.build_procedures
            ]

def from_module(m):
    return util.init_from_module(Project, m)
