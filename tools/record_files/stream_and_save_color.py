import pyrealsense2 as rs
import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display
from time import time



'''
Records a .avi video file with 300 frames in it, this video is blacked out and only contains the object of interest in it.
there are 6 things going on in this file:
    1. the sony a6000 streams very high resolution color video
    3. we process the color video from the sony to find the object of interest
    4. we get the region of interest using the processed image (or set it to 0)
    5. we save those processed images in an .avi video file
    6. we show in real-time the images that we are saving and draw the region of interest around the object of interest 
'''

def get_video(url):

    # initializes the video capture from the sony camera
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
            count += 1
            # get the color image from the Sony camera
            ret, color_image = cap.read()

            out.write(color_image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif count >= 400:
                break

        # saves the video
        cv2.destroyAllWindows()
        cap.release()


    finally:
        print("completed")
        cap.release()
