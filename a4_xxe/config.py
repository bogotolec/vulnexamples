from lxml.etree import Resolver, ParseError


DEFAULT_SIZE = 20
DEFAULT_MINES = 50


class OnlyOneURLResolver(Resolver):
    AVAILABLE_URL = 'file:///TODO.txt'
    SECRET = '\nTODO: fix XXE\nTODO: some-secret-data'

    def resolve(self, url, id, context):
        if url == self.AVAILABLE_URL:
            return self.resolve_string(self.SECRET, context)
        else:
            raise ParseError('Access to %s denied. ' % url +
                             'Available URLs: %s ' % self.AVAILABLE_URL,
                             None, None, 0)
