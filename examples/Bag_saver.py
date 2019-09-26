import pyrealsense2 as rs
import numpy as np
import cv2
import time

def save_bag():

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Increases the resolution of the images (update Chunk.py if you change those settings)
    # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    # config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

    # This will save the color and depth recording as a .bag
    config.enable_record_to_file("F:/realsense/dirty_clothing"+str(time.time())+'object_detection.bag')

    # Start streaming
    pipeline.start(config)


    e1 = cv2.getTickCount()

    try:
        while True:

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Apply colormap on depth image (image must be converted to8-bit per pixel first)
            # This is just for viewing purposes, these settings are not saved in the .bag file
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.16), cv2.COLORMAP_JET)

            # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            cv2.waitKey(1)
            e2 = cv2.getTickCount()
            t = (e2 - e1) / cv2.getTickFrequency()
            if t>19: # records for 10 seconds
                print("Done!")
                break

    finally:

        # Stop streaming
        pipeline.stop()