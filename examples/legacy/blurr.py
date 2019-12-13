import cv2
import sys
import os
import random

sys.path.insert(1, '../.')
import ailu_python.utils.tmp as func
import ailu_python.image_processing.getROI as getROI
import ailu_python.utils.display as display
import ailu_python.data_augmentation.modify_background as modBackground
import Workers

canvas = cv2.imread("./data/Image_resources_data_augmentation/canvas.png")

directory = "F:/AILU_RAW/weeds/FP-training-extracted/"
path_to_background = "F:/Data_aug_backgrounds/"
backgrounds = os.listdir(path_to_background)
print("Loaded", len(backgrounds), "background images")
count = 0
total = 0
train_dataset = True
# open video from avi file


for filename in os.listdir(directory):
    print("processing file: ", directory + filename)
    count = 0

    cap = cv2.VideoCapture(directory + filename)
    while cap.isOpened():

        # read each frame
        ret, frame = cap.read()
        count += 1

        rois_img = func.getAllRoiImage(frame)
        height, width = rois_img[0].shape[:2]
        #
        # resizedFrame = cv2.resize(rois_img[0], (int(width/10), int(height/10)))
        # resizedFrame = cv2.resize(resizedFrame, (width, height))
        # if height > 200 and width > 200:
        # print(height, width)
        try:
            blurred_frame = cv2.GaussianBlur(rois_img[0],(13,13),cv2.BORDER_DEFAULT)
        except:
            print("error blurring the image")


        display.draw_and_show(blurred_frame, [[0,0,0,0]], "rois")
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break


cv2.destroyAllWindows()




