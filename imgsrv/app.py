import json
import mimetypes

from flask import Flask, Response

from ladder import get_resolver

from oii.utils import memoize
from oii.webapi.utils import UrlConverter
from oii.webapi.image_service.utils import image_response
from oii.image.io import imread

ROOTS=[
    '/mnt/david3/habcam/assignment_images/proc',
    '/mnt/david4/habcam/ROIs'
]

# configure app
app = Flask(__name__)
app.url_map.converters['url'] = UrlConverter

# ladder access
@memoize(ttl=30)
def R():
    return get_resolver('imgsrv/resolver.xml').imgsrv

# endpoints
@app.route('/image/<url:pid>')
def service(pid):
    for root in ROOTS:
        for s in R().find_file(pid=pid,root=root):
            path = s['file'] # actual path to file
            image = imread(path) # read image data
            # use a fake filename so image_response
            # can guess correct MIME type
            fake_filename = 'i.%s' % s['ext']
            return image_response(image, fake_filename)
    # didn't find anything
    abort(404)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8888,debug=True)
