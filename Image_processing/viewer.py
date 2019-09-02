import pyrealsense2 as rs
import numpy as np
import cv2
import time
from random import shuffle
import utils

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Uncomment that line to stream from the .bag file instead of the camera:
rs.config.enable_device_from_file(config, "./bag_files/object_detection.bag")

# Make sure the resolution settings match those of the .bag file

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


IMG_HEIGHT = 360
IMG_WIDTH = 640
DIVISOR = 16



def img_cuber(img):
    height_div = int(360 / DIVISOR)
    width_div = int(640 / DIVISOR)
    posY = 0
    posX = 0
    
    cube_img = []
    
    for i in range(DIVISOR):
        for j in range(DIVISOR):
            roi = img[posY:posY+height_div, posX:posX+width_div]
            posY += height_div
            cube_img.append(roi)
            
        posX += width_div
        posY = 0
        
        
    shuffle(cube_img)

    posY = 0
    posX = 0
    
    count = 0
    
    for i in range(DIVISOR):
        for j in range(DIVISOR):
            img[posY:posY+height_div, posX:posX+width_div] = cube_img[count]
#             print(count)
            count += 1
            posY += height_div
            cube_img.append(roi)
            
        posX += width_div
        posY = 0
        
    return img

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

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        rois = utils.getROI(depth_image)

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=alphaKey), cv2.COLORMAP_JET)
        # depth_colormap = cv2.blur(depth_colormap, (30, 30))

        # viewImage(depth_colormap)

        hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)



        # hsv_depth = object_mask(hsv_depth)
        #
        #
        # gray_depth = cv2.cvtColor(hsv_depth, cv2.COLOR_BGR2GRAY)
        # ret, threshold = cv2.threshold(gray_depth, 240, 255, 0)
        # cv2.imshow('normal', threshold)
        #
        # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        # threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, rect_kernel)
        #
        # rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 80))
        # threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, rect_kernel)
        #
        # cv2.imshow('threshed', threshold)
        # contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        # img2 = color_image.copy()
        # for c in contours:
        #
        #     area = cv2.contourArea(c)
        #     if area > 1000:
        #         x, y, w, h = cv2.boundingRect(c)
        #         roi = color_image[y:y+h, x:x+w]
        #         img2 = img_cuber(img2)
        #         img2[y:y+h, x:x+w]=roi
        #         cv2.rectangle(color_image,(x,y),(x+w,y+h),(0,255,0),3)
        #         cv2.rectangle(hsv_depth,(x,y),(x+w,y+h),(0,255,0),3)

        for roi in rois:
            x1 = roi[0]
            y1 = roi[1]
            x2 = roi[2]
            y2 = roi[3]
            cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.rectangle(hsv_depth, (x1, y1), (x2, y2), (0, 255, 0), 3)

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)

        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

    cv2.destroyAllWindows()
    
finally:

    # Stop streaming
    pipeline.stop()





