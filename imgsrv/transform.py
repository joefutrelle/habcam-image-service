import re

import numpy as np

from skimage import img_as_float
from skimage.color import rgb2gray

from oii.image.transform import rescale
from oii.image.color import scale_saturation
from oii.image.stereo import get_L, get_R, swap_LR, redcyan
from imgsrv.stereo import anaglyph

def apply_tags(image, tags):
    h,w = image.shape[:2]
    if 'L' in tags:
        image = get_L(image)
    elif 'R' in tags:
        image = get_R(image)
    elif 'RL' in tags:
        image = swap_LR(image)
    elif 'redcyan' in tags:
        image = redcyan(rgb2gray(image),correct_y=True)
    elif 'anaglyph' in tags:
        image = anaglyph(image,correct_y=True)
    return image

def extract_roi(image, params):
    d = dict(params)
    h,w = image.shape[:2]
    if 'roicoords' in d:
        rx, ry, rw, rh = map(float, re.split(r',',d['roicoords']))
    else:
        rx = float(d.get('roixmin',0))
        ry = float(d.get('roiymin',0))
        rw = float(d.get('roiwidth',w-rx))
        rh = float(d.get('roiheight',h-ry))
    rxw = int(rx + rw)
    ryh = int(ry + rh)
    rx = int(rx)
    ry = int(ry)
    if rx==0 and ry==0 and rxw==w and ryh==h:
        return image
    else:
        return image[ry:ryh,rx:rxw,:]

def transform_image(image, params=[], tags=[]):
    image = apply_tags(image, tags)
    image = extract_roi(image, params)
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
