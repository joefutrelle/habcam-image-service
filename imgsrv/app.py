import json

from flask import Flask, Response

from ladder import get_resolver

from oii.utils import memoize
from oii.webapi.utils import UrlConverter

# configure app
app = Flask(__name__)
app.url_map.converters['url'] = UrlConverter

# ladder access
@memoize(ttl=30)
def R():
    return get_resolver('imgsrv/resolver.xml').imgsrv

# endpoints
@app.route('/image/<url:pid>')
def index(pid):
    solutions = list(R().pid(pid=pid))
    return Response(json.dumps(solutions),mimetype='application/json')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8888,debug=True)
