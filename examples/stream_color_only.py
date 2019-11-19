
import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display

cap = cv2.VideoCapture("C:/Users/andre/Desktop/FP-training1574022392.9003828output.avi")

while True:
    ret, color_image = cap.read()

    # color_image = cv2.resize(color_image, (640, 360))

    # blacked_color_img = getObject.using_blue(color_image)
    blacked_color_img = getObject.keep_green(color_image)
    rois = getROI.using_color(blacked_color_img)

    roi = rois[0]
    x1 = roi[0]
    y1 = roi[1]
    x2 = roi[2]
    y2 = roi[3]

    bdn_box = blacked_color_img[y1: y2, x1: x2]

    if bdn_box.shape[0] !=0:
        display.draw_and_show(bdn_box, [[0,0,0,0]], "blacked out image")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()










