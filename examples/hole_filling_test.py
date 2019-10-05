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


config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

profile = pipeline.start(config)

depth_sensor = profile.get_device().first_depth_sensor()
depth_sensor.set_option(
    rs.option.visual_preset, 3
)  # Set high accuracy for depth sensor
depth_scale = depth_sensor.get_depth_scale()


# Align the depth and color images
# align_to = rs.stream.color
# align = rs.align(align_to)

# This determines the threshold distance
alpha = 0.16
chunk_list = []
# Start streaming
try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        # aligned_frames = align.process(frames)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame:
            raise RuntimeError("Could not acquire depth or color frames.")

        decimation = rs.decimation_filter()
        decimation.set_option(rs.option.filter_magnitude, 4)

        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.filter_magnitude, 5)
        spatial.set_option(rs.option.filter_smooth_alpha, 1)
        spatial.set_option(rs.option.filter_smooth_delta, 50)
        spatial.set_option(rs.option.holes_fill, 3)
        depth_frame = spatial.process(depth_frame)

        frame = decimation.process(depth_frame)

        temporal = rs.temporal_filter()
        depth_frame = temporal.process(depth_frame)

        hole_filling = rs.hole_filling_filter()
        depth_frame = hole_filling.process(depth_frame)

        depth_image = np.asanyarray(depth_frame.get_data())
        depth_image = cv2.resize(depth_image, (1920, 1080))


        ret, color_image = cap.read()


        # blacked_color_img = getObject.using_depth_and_green(color_image, depth_image, 0.16)
        blacked_color_img = getObject.using_blue(color_image)
        # blacked_color_img = getObject.keep_green(blacked_color_img)
        rois = getROI.using_color(blacked_color_img)

        display.draw_and_show(blacked_color_img, rois, "blacked out image")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


finally:

    # Stop streaming
    pipeline.stop()





