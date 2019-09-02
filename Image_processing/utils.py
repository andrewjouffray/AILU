import numpy as np
import cv2

def object_mask(hsv_img):

    keepl = np.array([93, 235, 234])
    keeph = np.array([133, 275, 274])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    hsv_img[keep_mask > 0] = ([255,255,255])

    return hsv_img


def viewImage(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def getROI(depth_image):

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.16), cv2.COLORMAP_JET)
    # print(depth_colormap)
    hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)
    hsv_depth = object_mask(hsv_depth)

    gray_depth = cv2.cvtColor(hsv_depth, cv2.COLOR_BGR2GRAY)
    ret, threshold = cv2.threshold(gray_depth, 240, 255, 0)

    normal = threshold

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, rect_kernel)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (60, 60))
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, rect_kernel)

    filtered = threshold

    images = np.hstack((normal, filtered))

    # Show images
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('threshold images', images)

    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    valid_contours = []

    for c in contours:

        area = cv2.contourArea(c)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(c)
            xy_coordinates = [x, y, x+w, y+h]
            valid_contours.append(xy_coordinates)

    if valid_contours:
        return valid_contours
    else:
        return [[0,0,0,0]]