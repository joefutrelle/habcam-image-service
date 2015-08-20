import re

def parse_params(path, **defaults):
    """Parse a path fragment and convert to dict.
    Slashes separate alternating keys and values.
    For example /a/3/b/5 -> { 'a': '3', 'b': '5' }.
    Any keys not present get default values from **defaults"""
    parts = re.split('/',path)
    d = dict(zip(parts[:-1:2], parts[1::2]))
    for k,v in defaults.items():
        if k not in d:
            d[k] = v
    return d
