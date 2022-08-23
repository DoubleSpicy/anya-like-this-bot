import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

tv_size = (600, 780)

def image_resize(image, width = None, height = None, inter = cv.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


# def resize_v2():

target = cv.imread(r'./resources/typhoon.jpg', 1)
target = image_resize(target, height=500, width=650)
# target = cv.resize(target, (650, 650))
target2 = np.zeros((1080, 1728, 3), np.uint8)
print(target2.shape)
print(target.shape)
offset_y = round((target2.shape[0]/2 - target.shape[0]/2))
offset_x = round((target2.shape[1]/2 - target.shape[1]/2)) 
print(offset_y, offset_x)
target2[160:160+target.shape[0], 505: 505+target.shape[1]] = target
cv.imshow('target', target2)


src = cv.imread(r'./resources/base.jpg')
imgRGB = cv.cvtColor(src, cv.COLOR_BGR2RGB)
imgHSV = cv.cvtColor(imgRGB, cv.COLOR_BGR2HSV)

lower = np.array([60, 240, 245])    #Lower values of HSV range; Green have Hue value equal 120, but in opencv Hue range is smaler [0-180]
upper = np.array([70, 255, 255])  #Uppervalues of HSV range
imgRange = cv.inRange(imgHSV, lower, upper)

# kernels for morphology operations
kernel_noise = np.ones((3,3),np.uint8) #to delete small noises
kernel_dilate = np.ones((23,23),np.uint8)  #bigger kernel to fill holes after ropes
kernel_erode = np.ones((14,14),np.uint8)  #bigger kernel to delete pixels on edge that was add after dilate function

imgErode = cv.erode(imgRange, kernel_noise, 1)
imgDilate = cv.dilate(imgErode , kernel_dilate, 1)
imgErode = cv.erode(imgDilate, kernel_erode, 1)


mask = cv.cvtColor(imgErode, cv.COLOR_GRAY2BGR)
res = cv.subtract(src, mask)
# cv.imshow('res', res)

# mask of target
res_t = cv.bitwise_and(target2, target2, mask = imgErode)

res_f = cv.add(res, res_t)
cv.imshow('final', res_f)
# cv.imshow('res_t', res_t)


cv.waitKey(0)