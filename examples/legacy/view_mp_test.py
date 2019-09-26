# %%
## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import cv2
import numpy as np
import pyrealsense2 as rs
import Workers
import multiprocessing as mp


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

def object_mask(hsv_img):
    keepl = np.array([93, 235, 234])
    keeph = np.array([133, 275, 274])
    keep_mask = cv2.inRange(hsv_img, keepl, keeph)
    hsv_img[keep_mask > 0] = ([255,255,255])

    return hsv_img

if __name__ == '__main__':
    # Start streaming
    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_sensor.set_option(
        rs.option.visual_preset, 3
    )  # Set high accuracy for depth sensor
    depth_scale = depth_sensor.get_depth_scale()

    align_to = rs.stream.color
    align = rs.align(align_to)

    im_count = 0
    image_chunk = []

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
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.16), cv2.COLORMAP_JET)

            hsv_depth = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2HSV)

            hsv_depth = object_mask(hsv_depth)

            gray_depth = cv2.cvtColor(hsv_depth, cv2.COLOR_BGR2GRAY)
            ret, threshold = cv2.threshold(gray_depth, 0, 255, 0)

            contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

            for c in contours:

                area = cv2.contourArea(c)
                if area > 1000:
                    x, y, w, h = cv2.boundingRect(c)
                    #                     print(x, y, w, h)
                    cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.rectangle(hsv_depth, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Stack both images horizontally
            images = np.hstack((color_image, hsv_depth))

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)


            image_chunk.append(color_image)

            if len(image_chunk) >= 300:
                print("chunk full, starting processes")
                jobs = []
                for i in range(len(image_chunk)):
                    #                     p = mp.Process(target=save_image, args=(image_chunk[i]))
                    p = mp.Process(target=Workers.save_images, args=(image_chunk[i],))
                    jobs.append(p)
                    p.start()
                p.join()
                im_count = 0
                image_chunk = []
                print('Images saved, chunk cleared')

            #         cv2.imshow('RealSense', threshold)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        pipeline.stop()
        cv2.destroyAllWindow()
    except Exception as e:
        print(e)

    finally:

        # Stop streaming
        pipeline.stop()

# %%
