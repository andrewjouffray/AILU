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

directory = "F:/AILU_RAW/ar-codes/training-augmented/"
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

        rand_scale1 = random.uniform(0.5, 0.8)
        rand_scale2 = random.uniform(0.3, 1)
        rand_scale3 = random.uniform(0.3, 0.8)

        rand_rotate1 = random.randint(1, 360)
        rand_rotate2 = random.randint(1, 360)
        rand_rotate3 = random.randint(1, 360)

        rand_y1 = random.randint(1, 1080)
        rand_y2 = random.randint(1, 1080)
        rand_y3 = random.randint(1, 1080)

        # read each frame
        ret, frame = cap.read()
        count += 1
        if count % 10 == 0 or train_dataset == True:
            if ret == True:
                try:
                    new_canvas = canvas.copy()

                    total = count * 3

                    height, width = frame.shape[:2]

                    rois_img = func.getAllRoiImage(frame)

                    # for roi in rois_img:
                    #     display.draw_and_show(roi, [[0,0,0,0]], "rois")


                    if rois_img[0] is None:
                        print("rois[0] is None")

                    if rois_img[0].any() < 1 and len(rois_img) > 2:
                        print("roi[0] empty")
                        rois_img[0] = rois_img[1]
                    elif rois_img[0].any() < 1:
                        print("no roi at all")



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


                    new_canvas[rand_y1:rand_y1+height1, :width1] = scaled1
                    new_canvas[rand_y2:rand_y2+height2, width1:width1+width2] = scaled2
                    new_canvas[rand_y3:rand_y3+height3, width1+width2:width1+width2+width3] = scaled3

                    # display.draw_and_show(new_canvas, [[0, 0, 0, 0]], "rois")


                except Exception as e:
                    print("\nsize error:", e)
                    # print(rand_y1, rand_y1+height1)
                    # print(rand_y2,rand_y2+height2)
                    # print(rand_y3,rand_y3+height3)

                # # gets the coordinates of the roi
                rois = getROI.using_color(new_canvas)
                # display.draw_and_show(new_canvas, rois, "rois")

                try:
                    background_image = []
                    background_image_filename = backgrounds[random.randint(0, len(backgrounds) - 1)]
                    background_image = cv2.imread(path_to_background + background_image_filename)

                    while background_image is None:
                        background_image_filename = backgrounds[random.randint(0, len(backgrounds) - 1)]
                        background_image = cv2.imread(path_to_background + background_image_filename)

                    # add the background
                    frame_with_background = modBackground.black_to_image(new_canvas, background_image)

                    Workers.save_images(frame_with_background, rois, "F:/AILU_RAW/ar-codes/training-augmented/", "ar-codes")

                    # draws the roi on the image
                    # display.draw_and_show(frame_with_background, rois, 'frame from new_canvas')
                except Exception as e:
                    print(path_to_background + background_image_filename)
                    print("background_image",background_image)
                    print("Bearking Here:", e)



                # print("original images:", count, "augmented images:", total)

                # press 'q' to exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        else:
            continue
    else:
        continue