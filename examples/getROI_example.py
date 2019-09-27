import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.utils.display as display

# open video from avi file
cap = cv2.VideoCapture('./data/output.avi')
while True:

    # read each frame
    ret, frame = cap.read()

    # gets the coordinates of the roi
    rois = getROI.using_color(frame)

    # draws the roi on the image
    display.draw_and_show(frame, rois, 'frame from video')

    # press 'q' to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break