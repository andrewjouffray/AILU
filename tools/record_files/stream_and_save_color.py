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

            # process the color and depth image to isolate the object of interest, returns the "blacked out" image
            # blacked_color_img = getObject.using_blue(color_image)

            # get the region of interest from the blacked out image
            # rois = getROI.using_color(blacked_color_img)

            # add the image to the video that we are saving
            out.write(color_image)

            # show the blacked out image and draw the roi around the object of interest at the same time
            # display.draw_and_show(color_image, [[0,0,0,0]], "color image")

            print(count)


            # stop recording and save teh video id we hit the 'q' key or reach 300 images taken
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
        # Stop streaming
        # pipeline.stop()