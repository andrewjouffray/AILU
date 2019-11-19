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
    1. the intel realsense stream depth and color video (we only use the depth video)
    2. the sony NEXT 5T streams very high resolution color video
    3. we process the depth video from the intel and the color video from the sony to find the object of interest
    4. we get the region of interest using the processed image
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

    # # configures the depth streams and color streams from intel realsense
    # pipeline = rs.pipeline()
    # config = rs.config()
    # config.enable_stream(rs.stream.depth, 640, 360, rs.format.z16, 30)
    # config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
    #
    # # start steaming intel realsense
    # profile = pipeline.start(config)
    #
    # # align the depth and color frames coming from intel realsense
    # depth_sensor = profile.get_device().first_depth_sensor()
    # depth_sensor.set_option(
    #     # Set high accuracy for depth sensor
    #     rs.option.visual_preset, 3
    # )
    # align_to = rs.stream.color
    # align = rs.align(align_to)

    # count used to stop the loop at a certain time
    count = 0

    try:
        while True:
            count += 1
            # Wait for a coherent pair of frames: depth and color
            # frames = pipeline.wait_for_frames()
            # aligned_frames = align.process(frames)
            # aligned_depth_frame = aligned_frames.get_depth_frame()
            # color_frame = aligned_frames.get_color_frame()
            #
            # if not aligned_depth_frame or not color_frame:
            #     raise RuntimeError("Could not acquire depth or color frames.")
            #
            # # process the depth frame to fill holes and missing pixels
            # temporal = rs.temporal_filter()
            # aligned_depth_frame = temporal.process(aligned_depth_frame)
            # hole_filling = rs.hole_filling_filter()
            # aligned_depth_frame = hole_filling.process(aligned_depth_frame)
            #
            # # get the gray-scale depth image
            # depth_image = np.asanyarray(aligned_depth_frame.get_data())

            # get the color image from the Sony camera
            ret, color_image = cap.read()

            # process the color and depth image to isolate the object of interest, returns the "blacked out" image
            # blacked_color_img = getObject.using_blue(color_image)

            # get the region of interest from the blacked out image
            # rois = getROI.using_color(blacked_color_img)

            # add the blacked out image to the video that we are saving
            out.write(color_image)

            # show the blacked out image and draw the roi around the object of interest at the same time
            display.draw_and_show(color_image, [[0,0,0,0]], "color image")

            # stop recording and save teh video id we hit the 'q' key or reach 300 images taken
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif count >= 630:
                break

        # saves the video
        out.release()

        cv2.destroyAllWindows()


    finally:
        print("yooh")
        # Stop streaming
        # pipeline.stop()