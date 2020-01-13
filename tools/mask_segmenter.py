import numpy as np
import cv2
import sys
sys.path.insert(1, '../.')
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display
from time import time, sleep
import os
from tempfile import TemporaryFile

bounds = [[0,0,0], [0,0,0]]
old_bounds = []
current_bounds = []
mask_list = []
keeph = [None, None, None]
keepl = [None, None, None]

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
        upper = [pixel[0] + 10, pixel[1] + 10, pixel[2] + 10]
        lower = [pixel[0] - 10, pixel[1] - 10, pixel[2] - 10]
        mask_list.append([upper, lower])
        getBounds(mask_list)
        print(keeph, keepl)
    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(mask_list) > 0:
            print("deleted", mask_list[-1])
            del mask_list[-1]
            getBounds(mask_list)
            print(keeph, keepl)

def pauseVideo():
    while True:
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break

def getBounds(mask_list):

    for masks in mask_list:

        # if the keep values are none, set them to what ever color values are in mask_list
        if not keepl[0]:
            keepl = masks[1]
            keeph = masks[0]

        # finds the lowest values in mask_list and updates keepl
        if masks[1][0] < keepl[0]:
            keepl[0] = masks[1][0]
        if masks[1][1] < keepl[1]:
            keepl[1] = masks[1][1]
        if masks[1][2] < keepl[2]:
            keepl[2] = masks[1][2]

        # finds the highest values in mask_list and updates keeph
        if masks[0][0] > keeph[0]:
            keeph[0] = masks[0][0]
        if masks[0][1] > keeph[1]:
            keeph[1] = masks[0][1]
        if masks[0][2] > keeph[2]:
            keeph[2] = masks[0][2]

        keepl = np.asanyarray(keepl)
        keeph = np.asanyarray(keeph)




def apply_mask(hsv):



    # blacks out everything except the values between keepl and keeph
    if keepl[0]:
        keep_mask = cv2.inRange(hsv, keepl, keeph)
        res = cv2.bitwise_and(hsv, hsv, mask=keep_mask)
        image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

        return image
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return image

for filename in os.listdir(path_to_file):

    try:
        cap = cv2.VideoCapture(path_to_file+filename)

        while cap.isOpened():
            ret, color_image = cap.read()

            color_image = cv2.resize(color_image,(960, 720))
            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            masked_image = hsv.copy()
            masked_image = apply_mask(masked_image)

            bounds[0] = keepl
            bounds[1] = keeph

            rois = getROI.using_color(masked_image)
            images = np.hstack((color_image, masked_image))

            cv2.setMouseCallback("output", set_mask)
            cv2.imshow('output', images)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(20) & 0xFF == ord(' '):
                pauseVideo()


        cv2.destroyAllWindows()

    except Exception as e:
        print(e)

np.save('bounds', bounds)
print("saved the array")