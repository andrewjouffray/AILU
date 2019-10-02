import cv2
import sys

sys.path.insert(1, '../.')

import ailu_python.image_processing.getROI as getROI
import ailu_python.utils.display as display
import ailu_python.utils.tmp as func
import ailu_python.data_augmentation.modify_background as modBackground

# open video from avi file
cap = cv2.VideoCapture('./data/1569604389.9166079output.avi')
while True:

    # read each frame
    ret, frame = cap.read()

    height, width = frame.shape[:2]

    rois_img = getROI.getRoiImage(frame)

    tmp = func.scale_image(rois_img[0], 0.5)

    # # gets the coordinates of the roi
    rois = getROI.using_color(tmp)

    # draws the roi on the image
    display.draw_and_show(tmp, rois, 'frame from video')

    # press 'q' to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break