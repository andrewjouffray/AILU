import numpy as np
import pyrealsense2 as rs
import Workers
import Utils
import cv2

# Loads the bag files, processes each images and saves them with their XML file
def loadChunk(file_name, alpha, save_dir):
    pipeline = rs.pipeline()
    config = rs.config()

    rs.config.enable_device_from_file(config, "./"+file_name)

    # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    # config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    profile = pipeline.start(config)

    align_to = rs.stream.color
    align = rs.align(align_to)

    im_count = 0
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
            print("problem here")
            raise RuntimeError("Could not acquire depth or color frames.")

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Gets the regions of interest in the image
        rois = Utils.getROI(depth_image, alpha)

        # for roi in rois:
        #     x1 = roi[0]
        #     y1 = roi[1]
        #     x2 = roi[2]
        #     y2 = roi[3]
        #     cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 3)



        im_count += 1
        # Saves the images along with their XML files
        Workers.save_images(color_image, rois, save_dir)

        # Breaks the loop after 300 image
        if im_count == 570:
            print("STOP")
            break



