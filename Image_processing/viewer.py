import pyrealsense2 as rs
import numpy as np
import cv2
import time
from random import shuffle
import Utils

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Do you want to stream video from the camera or from a file?
from_camera = True

if from_camera:

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(
        rs.option.visual_preset, 3
    )  # Set high accuracy for depth sensor
    depth_scale = depth_sensor.get_depth_scale()

else:
    # Load video from a .bag file
    rs.config.enable_device_from_file(config, "F:/AILU_data/bag_files/1567530161.3578224object_detection.bag")

    # Make sure the resolution settings match those of the .bag file
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    profile = pipeline.start(config)

# Align the depth and color images
align_to = rs.stream.color
align = rs.align(align_to)


# This determines the threshold distance
alpha = 0.16


# Start streaming
alphaKey = 0.12
chunk_list = []

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
            raise RuntimeError("Could not acquire depth or color frames.")

        decimation = rs.decimation_filter()
        decimation.set_option(rs.option.filter_magnitude, 4)

        frame = decimation.process(aligned_depth_frame)

        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.filter_magnitude, 5)
        spatial.set_option(rs.option.filter_smooth_alpha, 1)
        spatial.set_option(rs.option.filter_smooth_delta, 50)
        aligned_depth_frame = spatial.process(aligned_depth_frame)

        temporal = rs.temporal_filter()
        aligned_depth_frame = temporal.process(aligned_depth_frame)

        hole_filling = rs.hole_filling_filter()
        aligned_depth_frame = hole_filling.process(aligned_depth_frame)

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        rois = Utils.getROI(depth_image, alpha)

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=alphaKey), cv2.COLORMAP_JET)
        hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)

        # for roi in rois:
        roi = rois[0]
        x1 = roi[0]
        y1 = roi[1]
        x2 = roi[2]
        y2 = roi[3]
        cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.rectangle(hsv_depth, (x1, y1), (x2, y2), (0, 255, 0), 3)

        # Stack both images horizontally
        # images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('color_image', color_image)
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('depth_colormap', depth_colormap)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

    cv2.destroyAllWindows()
    
finally:

    # Stop streaming
    pipeline.stop()





