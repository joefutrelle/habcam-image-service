import json
import mimetypes
import re

from flask import Flask, Response, abort

from ladder import get_resolver

from imgsrv.utils import ParamsConverter
from imgsrv.transform import transform_image

from oii.utils import memoize
from oii.webapi.utils import UrlConverter
from oii.webapi.image_service.utils import image_response
from oii.image.io import imread

from config_imgsrv import ROOTS

# configure app
app = Flask(__name__)
app.url_map.converters['url'] = UrlConverter
app.url_map.converters['params'] = ParamsConverter

# ladder access
@memoize(ttl=30)
def R():
    return get_resolver('imgsrv/resolver.xml').imgsrv

def parse_tags(tags):
    if tags is None:
        return []
    return re.split(r'_',tags)

# finds and reads an image given a pid,
# then applies params-based transformations,
# then returns the image response
def pid2image(pid='',params=[]):
    for root in ROOTS:
        for s in R().find_file(pid=pid,root=root):
            path = s['file'] # actual path to file
            tags = parse_tags(s.get('tags',None))
            image = imread(path) # read image data
            image = transform_image(image, params, tags)
            # use a fake filename so image_response
            # can guess correct MIME type
            fake_filename = 'i.%s' % s['ext']
            return image_response(image, fake_filename)
    # didn't find anything
    abort(404)

# endpoints

@app.route('/image/<params:params>/<url:pid>')
def serve_image_with_params(params,pid):
    return pid2image(pid, params)

@app.route('/image/<url:pid>')
def serve_image_no_params(pid):
    return pid2image(pid)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8888,debug=True)
