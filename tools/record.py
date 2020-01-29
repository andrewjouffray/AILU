
import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display
import stream_and_save_color

# cap = cv2.VideoCapture("E:/AILU_RAW/weeds/CQL-training/CQL-training1574203453.813714output.avi")
cap = cv2.VideoCapture(0)

while True:
    ret, color_image = cap.read()
    if ret:

        height, width, channels = color_image.shape




        color_image = cv2.resize(color_image, (int(width / 2), int(height / 2)))

        # color_image = getObject.using_blue(color_image)
        # color_image = getObject.keep_green(color_image)
        # rois = getROI.using_color(color_image)



        display.draw_and_show(color_image, [[0,0,0,0]], "blacked out image")

        k = cv2.waitKey(33)
        if k == 112:
            break
        elif k == 115:
            cap.release()
            folder = "C:/Users/andre/Pictures/Video Projects/"
            stream_and_save_color.get_video(folder)
    else:
        print("no image")
        cap = cv2.VideoCapture(0)
        ret, color_image = cap.read()


cv2.destroyAllWindows()










