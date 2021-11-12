
# Spin up ImageJ.
from skimage import data, io
from matplotlib import pyplot as plt
import imagej
ij = imagej.init('F:/NATIONAL TAIPEI UNIVERSITY OF TECHNOLOGY/fiji-win64/Fiji.app')


# Import an image with scikit-image.
import skimage
from skimage import io
# NB: Blood vessel image from: https://www.fi.edu/heart/blood-vessels
#img = io.imread('https://imagej.net/images/clown.png')
img = io.imread('C:/Users/USER/Downloads/8-bit - find edge - binary - close.tif')
img1 = img
import numpy as np
#img = np.mean(img, axis=2)
import cv2
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Invoke ImageJ's Frangi vesselness op.
vessels = np.zeros(img.shape, dtype=img.dtype)
ij.op().filter().frangiVesselness(ij.py.to_java(vessels), ij.py.to_java(img), [1, 1], 20)
ij.op().filter().gauss(ij.py.to_java(vessels), ij.py.to_java(img), 2)
print(vessels.dtype)
print(vessels.shape)
print(img.dtype)
print(img.shape)
cv2.namedWindow('vessels', cv2.WINDOW_NORMAL)
cv2.resizeWindow('vessels', 540, 540)
cv2.imshow('vessels', vessels)
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.resizeWindow('img', 540, 540)
cv2.imshow('img', img)

k = cv2.waitKey(0)
cv2.destroyAllWindows()
