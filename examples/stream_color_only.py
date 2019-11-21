
import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display

# cap = cv2.VideoCapture("E:/AILU_RAW/weeds/CQL-training/CQL-training1574203453.813714output.avi")
cap = cv2.VideoCapture(0)

while True:
    ret, color_image = cap.read()

    # color_image = cv2.resize(color_image, (640, 360))

    # color_image = getObject.using_blue(color_image)
    color_image = getObject.keep_green(color_image)
    rois = getROI.using_color(color_image)



    display.draw_and_show(color_image, [[0,0,0,0]], "blacked out image")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()










