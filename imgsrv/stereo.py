import numpy as np

from skimage.color import rgb2gray

from oii.image.stereo import align, rot90_LR

def anaglyph(rgb_LR,dx=None,correct_y=False):
    y_LR = rgb2gray(rgb_LR)
    (h,w2) = y_LR.shape
    w = w2/2
    if dx is None:
        dx = align(y_LR)
    if correct_y:
        dy = align(rot90_LR(y_LR,dx))
    else:
        dy = 0
    # align x
    rgb_LR[:,w:,:] = np.roll(rgb_LR[:,w:,:],dx/2,axis=1)
    rgb_LR = rgb_LR[:,dx/2:w2-dx/2,:]
    (h,w2) = rgb_LR.shape[:2]
    w = w2/2
    red = rgb_LR[:,:w,0]
    cyan = (rgb_LR[:,w:,1]/2) + (rgb_LR[:,w:,2]/2)
    # align y
    if dy != 0:
        cyan = np.roll(cyan,dy,axis=0)
    rolled = np.dstack([red,cyan,cyan])
    # crop
    if dy > 0:
        rolled = rolled[dy:,dx:,:]
    else:
        rolled = rolled[:-dy,dx:,:]
    return rolled
