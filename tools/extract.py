
import sys
sys.path.insert(1, '../.')
import ailu_python.image_processing.getROI as getROI
import cv2
from bounds import Bounds
import os
import numpy as np

def set_mask(event,x,y,_,__):

    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y, x]
        bounds.addColors(15, pixel)

    elif event == cv2.EVENT_RBUTTONDOWN:
        bounds.removeColors()

def pauseVideo():
    while True:
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break

def apply_mask(keeph, keepl, hsv):

    # blacks out everything except the values between keepl and keeph
    if not keepl is None:
        keep_mask = cv2.inRange(hsv, keepl, keeph)
        res = cv2.bitwise_and(hsv, hsv, mask=keep_mask)
        image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

        return image
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return image


bounds = Bounds()
path_to_file = "F:/data/weeds/RP-validation/"

for filename in os.listdir(path_to_file):


    cap = cv2.VideoCapture(path_to_file+filename)


    while cap.isOpened():
        ret, color_image = cap.read()

        color_image = cv2.resize(color_image,(960, 720))
        hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)


        colorRange = bounds.getBounds()
        keeph = colorRange[0]
        keepl = colorRange[1]

        masked_image = hsv.copy()
        masked_image = apply_mask(keeph, keepl, masked_image)


        rois = getROI.using_color(masked_image)
        images = np.hstack((color_image, masked_image))

        cv2.setMouseCallback("output", set_mask)
        cv2.imshow('output', images)

        k = cv2.waitKey(33)
        if k == 112:
            pauseVideo()
        elif k == 115:
            bounds.saveBounds('./')
        elif k == 113:
            break




cv2.destroyAllWindows()
