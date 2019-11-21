import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display
from time import time, sleep
import os
import sys

mask_list = []

if len(sys.argv) < 2:

    print("Missing arguments, (source) e.g. python extract_features.py C:/myVidel.avi")
    exit()

path_to_file = sys.argv[1]


# checks if the file exists
if not os.path.exists(path_to_file):
    print("could not find ", path_to_file)
    exit()

def set_mask(event,x,y,_,__):

    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y, x]

        # HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.
        upper = [pixel[0] + 20, pixel[1] + 20, pixel[2] + 20]
        lower = [pixel[0] - 20, pixel[1] - 20, pixel[2] - 20]
        mask_list.append([upper, lower])


def pauseVideo():
    while True:
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break

def apply_mask(mask_list, hsv):

    keepl = [300,300,300]
    keeph = [300,300,300]

    for masks in mask_list:

        if masks[1][0] < keepl[0]:
            keepl[0] = masks[1][0]
        if masks[1][1] < keepl[1]:
            keepl[1] = masks[1][1]
        if masks[1][2] < keepl[2]:
            keepl[2] = masks[1][2]

        if masks[0][0] > keeph[0]:
            keeph[0] = masks[0][0]
        if masks[0][1] > keeph[1]:
            keeph[1] = masks[0][1]
        if masks[0][2] > keeph[2]:
            keeph[2] = masks[0][2]


    keepl = np.asarray(keepl)
    keeph = np.asarray(keeph)
    keep_mask = cv2.inRange(hsv, keepl, keeph)
    res = cv2.bitwise_and(hsv, hsv, mask=keep_mask)
    image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

    return image


for filename in os.listdir(path_to_file):

    try:
        cap = cv2.VideoCapture(path_to_file+filename)

        while cap.isOpened():
            ret, color_image = cap.read()

            color_image = cv2.resize(color_image,(640, 360))
            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            masked_image = hsv.copy()
            masked_image = apply_mask(mask_list, masked_image)

            rois = getROI.using_color(masked_image)
            images = np.hstack((hsv, masked_image))

            cv2.setMouseCallback("output", set_mask)
            # cv2.imshow('input', hsv)

            cv2.imshow('output', images)

            # display.draw_and_show(masked_image, rois, "output")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(2) & 0xFF == ord(' '):
                pauseVideo()

        cv2.destroyAllWindows()

    except Exception as e:
        print(e)
        exit()

