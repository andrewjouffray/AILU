#!/usr/bin/env python
# coding: utf-8

# In[24]:


## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
import time
from random import shuffle

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# rs.config.enable_device_from_file(config, "../object_detection.bag")

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile = pipeline.start(config)

depth_sensor = profile.get_device().first_depth_sensor()
depth_sensor.set_option(
    rs.option.visual_preset, 3
)  # Set high accuracy for depth sensor
depth_scale = depth_sensor.get_depth_scale()

align_to = rs.stream.color
align = rs.align(align_to)


IMG_HEIGHT = 360
IMG_WIDTH = 640
DIVISOR = 16

HmargDiv = 7
VmargDiv = 4.4

hDiv = 0.82
lDiv= 0.82

vertical_margin = int(360 / VmargDiv)
horizonal_margin = int(640 / HmargDiv)
# horizonal_margin = 0
height = int(360 * hDiv)
length = int(640 * lDiv)

def viewImage(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def object_mask(hsv_img):
     
    # keepl = np.array([-20, 235, 108])
    # keeph = np.array([20, 275, 148])
    # keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # hsv_img[keep_mask > 0] = ([0,0,0])
    
    # keepl = np.array([100, 235, 108])
    # keeph = np.array([140, 275, 148])
    # keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    # hsv_img[keep_mask > 0] = ([0,0,0])

    keepl = np.array([93, 235, 234])
    keeph = np.array([133, 275, 274])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    hsv_img[keep_mask > 0] = ([255,255,255])

    return hsv_img


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


        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=alphaKey), cv2.COLORMAP_JET)
        # depth_colormap = cv2.blur(depth_colormap, (30, 30))

        # viewImage(depth_colormap)
        
        hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)


        hsv_depth = object_mask(hsv_depth)


        gray_depth = cv2.cvtColor(hsv_depth, cv2.COLOR_BGR2GRAY)
        ret, threshold = cv2.threshold(gray_depth, 240, 255, 0)
        cv2.imshow('normal', threshold)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, rect_kernel)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 80))
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, rect_kernel)

        cv2.imshow('threshed', threshold)
        contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        img2 = color_image.copy()
        for c in contours:
            
            area = cv2.contourArea(c)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(c)
                # # print(x, y, w, h)
                # x = int(x*1.15)
                # y = int(y-(y*0.2))
                # sw = int(w*1.30)
                # sh = int(h*1.30)
                # sx = int(x-(x*0.15))
                # sy = int(y-(y*0.15))
                # cv2.rectangle(color_image,(sx,sy),(x+sw,y+sh),(0,255,0),3)
                # cv2.rectangle(hsv_depth,(sx,sy),(x+sw,y+sh),(0,255,0),3)
                roi = color_image[y:y+h, x:x+w]
                img2 = img_cuber(img2)
                img2[y:y+h, x:x+w]=roi
                cv2.rectangle(color_image,(x,y),(x+w,y+h),(0,255,0),3)
                cv2.rectangle(hsv_depth,(x,y),(x+w,y+h),(0,255,0),3)

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        chunk_list.append(color_image)

        if len(chunk_list) >= 15:
            print("chunk full")
            chunk_list = []


#         cv2.imshow('RealSense', threshold)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF ==ord('o'):
            hDiv += 0.5
            print("raising hDiv", hDiv)

        elif cv2.waitKey(1) & 0xFF ==ord('p'):
            hDiv -= 0.5
            print("lowering hDiv", hDiv)

        elif cv2.waitKey(1) & 0xFF ==ord('u'):
            lDiv += 0.5
            print("raising lDiv", lDiv)

        elif cv2.waitKey(1) & 0xFF ==ord('i'):
            lDiv -= 0.5
            print("lowering lDiv", lDiv)

        elif cv2.waitKey(1) & 0xFF == ord('v'):
            print("saving img")
            cv2.imwrite("./imgs/" + str(time.time()) + ".png", color_image)
    cv2.destroyAllWindows()
    
finally:

    # Stop streaming
    pipeline.stop()


# In[ ]:




