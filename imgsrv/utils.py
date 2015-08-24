import re

from werkzeug.routing import BaseConverter

def parse_params(path):
    """Parse a path fragment and convert to a list of tuples.
    Slashes separate alternating keys and values.
    For example /a/3/b/5 -> [ ['a', '3'], ['b', '5'] ]."""
    parts = re.split('/',path)
    keys = parts[:-1:2]
    values= parts[1::2]
    return zip(keys,values)

class ParamsConverter(BaseConverter):
    def __init__(self, url_map):
        super(ParamsConverter, self).__init__(url_map)
        self.regex = r'(([^/]+/[^/]+/)*[^/]+/[^/]+)'
    def to_python(self, value):
        return parse_params(value)
    def to_url(self, value):
        return value

