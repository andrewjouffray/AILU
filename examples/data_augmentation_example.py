import cv2
import sys
import os
import random

sys.path.insert(1, '../.')

import ailu_python.image_processing.getROI as getROI
import ailu_python.utils.display as display
import ailu_python.utils.tmp as func
import ailu_python.data_augmentation.modify_background as modBackground

canvas = cv2.imread("./data/Image_resources_data_augmentation/canvas.png")

directory = "./data/good_milano/"
count = 0
total = 0
# open video from avi file
for filename in os.listdir(directory):

    cap = cv2.VideoCapture(directory + filename)
    while cap.isOpened():

        rand_scale1 = random.uniform(0.5, 1)
        rand_scale2 = random.uniform(0.5, 1.3)
        rand_scale3 = random.uniform(0.5, 1.3)

        rand_rotate1 = random.randint(1, 360)
        rand_rotate2 = random.randint(1, 360)
        rand_rotate3 = random.randint(1, 360)

        rand_y1 = random.randint(1, 1080)
        rand_y2 = random.randint(1, 1080)
        rand_y3 = random.randint(1, 1080)

        # read each frame
        ret, frame = cap.read()

        if ret == True:

            new_canvas = canvas.copy()

            count += 1
            total = count * 3

            height, width = frame.shape[:2]

            rois_img = func.getAllRoiImage(frame)
            copy0 = rois_img[0].copy()
            copy1 = rois_img[0].copy()

            scaled1 = func.scale_image(rois_img[0], rand_scale1)
            scaled2 = func.scale_image(copy1, rand_scale2)
            scaled3 = func.scale_image(copy0, rand_scale3)

            scaled1 = func.rotate_image(scaled1, rand_rotate1)
            scaled2 = func.rotate_image(scaled2, rand_rotate2)
            scaled3 = func.rotate_image(scaled3, rand_rotate3)

            height1, width1 = scaled1.shape[:2]
            height2, width2 = scaled2.shape[:2]
            height3, width3 = scaled3.shape[:2]

            if height1 + rand_y1 >= 1080:
                total_height = height1 + rand_y1
                difference = total_height - 1080
                rand_y1 = rand_y1 - difference
            if height2 + rand_y2 >= 1080:
                total_height = height2 + rand_y2
                difference = total_height - 1080
                rand_y2 = rand_y2 - difference
            if height3 + rand_y3 >= 1080:
                total_height = height3 + rand_y3
                difference = total_height - 1080
                rand_y3 = rand_y3 - difference

            try:
                new_canvas[rand_y1:rand_y1+height1, :width1] = scaled1
                new_canvas[rand_y2:rand_y2+height2, width1:width1+width2] = scaled2
                new_canvas[rand_y3:rand_y3+height3, width1+width2:width1+width2+width3] = scaled3
            except:
                print("error: \n")
                print(rand_y1, rand_y1+height1)
                print(rand_y2,rand_y2+height2)
                print(rand_y3,rand_y3+height3)

            # # gets the coordinates of the roi
            rois = [[0,0,0,0]]

            # draws the roi on the image
            display.draw_and_show(new_canvas, rois, 'frame from new_canvas')





            print("original images:", count, "augmented images:", total)

            # press 'q' to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break