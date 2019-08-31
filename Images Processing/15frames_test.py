import numpy as np
import pyrealsense2 as rs
import cv2

def viewImage(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    profile = pipeline.start(config)

    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    align_to = rs.stream.color
    align = rs.align(align_to)

    #   Init variables
    im_count = 0
    image_chunk = []
    image_chunk2 = []
    # sentinel = True
    try:
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
            viewImage(color_image)
            # Gets the region of interest in the image if there is one [[x1, y1, x2, y2]], returns False if there is none
            # valid_contours = Contourer.getROI(depth_image)
            # print(valid_contours)
            # print(color_image)
            # group = [color_image, valid_contours]
            # im_count += 1
            image_chunk.append(color_image)
            image_chunk2.append(depth_image)
            # print(ROI_coordinates)
            # cv2.imshow('image', color_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()1
            # if len(image_chunk) >= 25:
            #     for frame in image_chunk:
            #         color_image = np.asanyarray(frame.get_data())
            #         viewImage(color_image)


    except Exception as e:
        print(e)

    finally:
        # Stop streaming
        pipeline.stop()
