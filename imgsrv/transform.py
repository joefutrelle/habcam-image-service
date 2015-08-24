import numpy as np

from skimage import img_as_float

from oii.image.transform import rescale
from oii.image.color import scale_saturation

def transform_image(image, params=[]):
    for k,v in params:
        if k=='saturation':
            saturation = float(v)
            image = scale_saturation(image, saturation)
        elif k=='gamma':
            gamma = float(v)
            image = np.power(img_as_float(image), gamma)
        elif k=='brightness':
            b = float(v)
            image = (img_as_float(image) * b).clip(0.,1.)
        elif k=='width':
            scale = float(v) / image.shape[1]
            image = rescale(image, scale)
        elif k=='maxwidth':
            w = float(v)
            if image.shape[1] > w:
                scale = w / image.shape[1]
                image = rescale(image, scale)
        elif k=='height':
            scale = float(v) / image.shape[0]
            image = rescale(image, scale)
        elif k=='maxheight':
            h = float(v)
            if image.shape[0] > h:
                scale = h / image.shape[0]
                image = rescale(image, scale)
    return image
