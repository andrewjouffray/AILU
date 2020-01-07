import cv2
import sys
import numpy as np
import ailu_python.image_processing.getROI as getROI


def rotate_image(img, angle):

    height, width = img.shape[:2]
    image_center = (width/2, height/2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])

    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    rotated_mat = cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))
    return rotated_mat


def scale_image(img, zoom):

    height, width = img.shape[:2]
    image_center = (width/2, height/2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, 1. , zoom)

    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])

    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    rotated_mat = cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))
    return rotated_mat

def getAllRoiImage(image):
    rois = getROI.using_color(image)
    ret = []
    for roi in rois:
        x1 = roi[0]
        y1 = roi[1]
        x2 = roi[2]
        y2 = roi[3]
        ret.append(image[y1:y2, x1:x2])
    return ret

def lowerRes(image, factor):


    height, width = image.shape[:2]
    lowerResImage = cv2.resize(image, (int(width/factor), int(height/factor)))
    lowerResImage = cv2.resize(lowerResImage, (width, height))

    return lowerResImage

def blurr(image, kernelSize):

    if kernelSize % 2 == 0:
        kernelSize += 1

    blurred_frame = cv2.GaussianBlur(image, (kernelSize, kernelSize), cv2.BORDER_DEFAULT)

    return blurred_frame