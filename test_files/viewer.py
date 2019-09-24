import pyrealsense2 as rs
import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display


# Configure depth and color streams
cap = cv2.VideoCapture(2)
pipeline = rs.pipeline()
config = rs.config()

# Do you want to stream video from the camera or from a file?
from_camera = True
use_external_cam = 1

if from_camera:

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(
        rs.option.visual_preset, 3
    )  # Set high accuracy for depth sensor
    depth_scale = depth_sensor.get_depth_scale()

else:
    # Load video from a .bag file
    rs.config.enable_device_from_file(config, "E:/AILU_data/bag_files/1567530161.3578224object_detection.bag")

    # Make sure the resolution settings match those of the .bag file
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    profile = pipeline.start(config)

# Align the depth and color images
align_to = rs.stream.color
align = rs.align(align_to)


# This determines the threshold distance
alpha = 0.16
chunk_list = []
# Start streaming
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

        temporal = rs.temporal_filter()
        aligned_depth_frame = temporal.process(aligned_depth_frame)

        hole_filling = rs.hole_filling_filter()
        aligned_depth_frame = hole_filling.process(aligned_depth_frame)

        depth_image = np.asanyarray(aligned_depth_frame.get_data())

        if use_external_cam == 1:
            ret, color_image = cap.read()
        else:
            color_image = np.asanyarray(color_frame.get_data())

        blacked_color_img = getObject.using_depth_and_green(color_image, depth_image, 0.16)

        rois = getROI.using_color(blacked_color_img)

        display.draw_and_show(blacked_color_img, rois, "blacked out image")

        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

    cv2.destroyAllWindows()
    
finally:

    # Stop streaming
    pipeline.stop()





