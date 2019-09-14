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
red_exclusion = False

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
        if red_exclusion:
            rois = Utils.getROI_red_exclution(color_image, rois)

        Utils.draw_and_show(color_image, rois)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

    cv2.destroyAllWindows()
    
finally:

    # Stop streaming
    pipeline.stop()





