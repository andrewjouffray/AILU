import pyrealsense2 as rs
import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display
from time import time



'''
Records a .avi video file with a number of frames defined by FRAMES_LIMIT in it.
'''

def get_video(url):

    FRAMES_LIMIT = 400

    # initializes the video capture from the sony camera (change 0 to your camera's index)
    cap = cv2.VideoCapture(0)

    # configure cv2 to save the video in 1080p at 30 fps in .avi format
    height = 1080
    width = 1920
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    fps = 30
    video_filename = url + str(time()) + 'output.avi'
    out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

    count = 0

    try:
        while True:

            # get the color image from the Sony camera
            ret, color_image = cap.read()
            count += 1

            out.write(color_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                # stops if user presses q
                break
            elif count >= FRAMES_LIMIT:
                # stops if the frame limit is reached
                break

        # saves the video
        cv2.destroyAllWindows()
        cap.release()


    finally:
        print("completed")
        cap.release()
