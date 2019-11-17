
import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display

cap = cv2.VideoCapture(0)

while True:
    ret, color_image = cap.read()

    blacked_color_img = getObject.using_blue(color_image)
    # blacked_color_img = getObject.keep_green(blacked_color_img)
    rois = getROI.using_color(blacked_color_img)

    display.draw_and_show(blacked_color_img, rois, "blacked out image")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()










