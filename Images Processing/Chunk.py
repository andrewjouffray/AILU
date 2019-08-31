import cv2
import numpy as np
import pyrealsense2 as rs
# import Contourer
import cv2
import Workers

def viewImage(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def object_mask(hsv_img):
    keepl = np.array([93, 235, 234])
    keeph = np.array([133, 275, 274])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    hsv_img[keep_mask > 0] = ([255,255,255])

    return hsv_img


def loadChunk(file_name):
    pipeline = rs.pipeline()
    config = rs.config()

    rs.config.enable_device_from_file(config, "./"+file_name)

    # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    # config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    profile = pipeline.start(config)

    # depth_sensor = profile.get_device().first_depth_sensor()
    # depth_sensor.set_option(
    #     rs.option.visual_preset, 3
    # )  # Set high accuracy for depth sensor
    # depth_scale = depth_sensor.get_depth_scale()

    align_to = rs.stream.color
    align = rs.align(align_to)

    #   Init variables
    im_count = 0
    image_chunk = []
    big_chunk = []
    roi_chunk = []
    big_roi = []
    # sentinel = True
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
            # viewImage(color_image)


            # Gets the region of interest in the image if there is one [[x1, y1, x2, y2]], returns False if there is none
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.16), cv2.COLORMAP_JET)
            # print(depth_colormap)
            hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)
            hsv_depth = object_mask(hsv_depth)

            gray_depth = cv2.cvtColor(hsv_depth, cv2.COLOR_BGR2GRAY)
            ret, threshold = cv2.threshold(gray_depth, 240, 255, 0)

            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
            threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, rect_kernel)

            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (60, 60))
            threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, rect_kernel)

            contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            valid_contours = []

            for c in contours:
                area = cv2.contourArea(c)
                if area > 1000:
                    x, y, w, h = cv2.boundingRect(c)
                    # print(x, y, x+w, y+h)
                    xy_coordinates = [x, y, x + w, y + h]
                    cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    valid_contours.append(xy_coordinates)

            if not valid_contours:
                valid_contours = [[0, 0, 0, 0]]

            # print(valid_contours)
            # print(color_image)
            # if color_image:
            # image_chunk.append(color_image)
            # # else: print("no color image")
            # roi_chunk.append(valid_contours)
            im_count += 1
            Workers.save_images(color_image, valid_contours)
            # # print(ROI_coordinates)
            # # cv2.imshow('image', color_image)
            # # cv2.waitKey(0)
            # # cv2.destroyAllWindows()
            # if len(image_chunk) >= 300:
            #     # sentinel = False
            #     yield image_chunk, roi_chunk
            #     image_chunk = []
            #     roi_chunk = []
            if im_count == 300:
                print("STOP")
                break



