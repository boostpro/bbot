repositories = {}

class Repository(object):
    def __init__(self, url, properties=None):
        self.url = url
        self.properties = properties or {}
        repositories[url] = self

    def set_properties(self, include, exclude):
        for p in include:
            if p in self.properties:
                if not self.properties[p]:
                    raise ValueError, \
                        'property %s was already excluded from repository %s: %s' % (
                        p,self.url, self.properties)
            else:
                self.properties[p] = True

        for p in exclude:
            if p in self.properties:
                if self.properties[p]:
                    raise ValueError, \
                        'property %s was already included in repository %s: %s' % (
                        p,self.url, self.properties)
            else:
                self.properties[p] = False

class GitHub(Repository):
    def __init__(self, id):
        super(GitHub,self).__init__('https://github.com/%s' % id)

