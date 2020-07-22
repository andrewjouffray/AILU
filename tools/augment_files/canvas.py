'''
input: one single object of interest

step1: chose a height (360-1080)
step2: chose an aspect ratio [1.33, 1.66, 1.78, 1.85, 2.39]
step3: finds a background image
step4: fits the background image to the canvas size
step5: define the number of objects to insert
step6: create the objects
step7: add the objects onto the image
step8: modify the image (chance of lowering resolution or making it blurry)


'''
import sys
sys.path.insert(1, '../.')
import random
import cv2
from augment_files.ooi import Ooi
import time
import ailu_python.data_augmentation.modify_background as modBackground
import ailu_python.data_augmentation.transforms as transforms
import ailu_python.utils.display as display
import ailu_python.utils.tmp as func
import PIL
import numpy as np

class Canvas:

    __width = 0
    __height = 0
    __aspectRatio = 0
    __listOfAspectRatios = [1.33, 1.66, 1.78, 1.85, 2.39]
    # __listOfAspectRatios = [2.39]
    __objects = []
    __canvas = None
    __mask = None
    __rois = []

    def __init__(self, ooi, pathToCanvas, background, maxOoi = 10):

        # gets a random image height, aspect ration and width
        self.__height = random.randint(500, 720)
        # self.__height = 900
        self.__aspectRatio = self.__listOfAspectRatios[random.randint(0, len(self.__listOfAspectRatios) - 1)]
        self.__width = int(self.__height * self.__aspectRatio)
        self.__rois = []
        canvas = cv2.imread(pathToCanvas)

        # sets the canvas as the chosen background
        self.__canvas = canvas[:self.__height, :self.__width]

        # picks a random number of objects of interest to insert into the image
        numberOfOoi = random.randint(2, maxOoi)
        # print("number of ooi:", numberOfOoi)

        # divides the image into columns, one for each object of interest (ooi)
        columnWidth = int(self.__width / numberOfOoi)
        # print("column width:", columnWidth)


        # creates the objects of interest
        # in some cases, no ooi are created and put in the canvas, in that case, try again
        tries = 0
        while True:
            tries += 1
            for i in range(numberOfOoi):

                    # create a new object
                    objectOfinterest = Ooi(ooi, columnWidth, self.__height, columnWidth * i)
                    self.__objects.append(objectOfinterest)

                    # gets it's position
                    x1, y1, x2, y2 = objectOfinterest.getPosition()

                    # inserts the object into the column
                    try:
                        self.__canvas[y1:y2, x1:x2] = objectOfinterest.getObject()
                        # self.__rois.append([x1, y1, x2, y2])
                    except Exception as e:
                        pass
            self.__rois = func.getROI.using_color_on_canvas(self.__canvas)
            # checks if ooi were created, break the loop if yes.
            if self.__rois != [[0,0,0,0]]:
                # print("success", tries)
                break
            elif tries > 5:
                self.__objects = []
                self.__rois = []
                print("failed", self.__rois, tries)
                break
        self.__mask = modBackground.create_masks(self.__canvas, background)
        self.__canvas = modBackground.black_to_image(self.__canvas, background)


    def lowerRes(self):

        # allows to reduce the resolution more on larger images
        if self.__height > 720:
            factor = random.uniform(1, 2)
        else:
            factor = random.uniform(1, 1.5)
        lowerResImage = cv2.resize(self.__canvas, (int(self.__width / factor), int(self.__height / factor)))
        self.__canvas = cv2.resize(lowerResImage, (self.__width, self.__height))

    def blur(self):

        kernelSize = random.randint(1, 5)

        if kernelSize % 2 == 0:
            kernelSize += 1

        self.__canvas = cv2.GaussianBlur(self.__canvas, (kernelSize, kernelSize), cv2.BORDER_DEFAULT)

    def tint(self):

        colors = [[0, 255, 255], [255, 255, 0], [0, 255, 0], [255,0,0], [0,0,255], [255, 0, 255]]
        PIL_img = PIL.Image.fromarray(self.__canvas)
        color = colors[random.randint(0, len(colors) -1)]
        PIL_img = transforms.RGBTransform().mix_with((color[0], color[1], color[2]), factor=random.uniform(0.05, 0.3)).applied_to(PIL_img)
        self.__canvas = np.array(PIL_img)

    # changes the gamma (brightness of the image)
    def changeGamma(self):

        gamma = random.uniform(0.8, 2)
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        self.__canvas = cv2.LUT(self.__canvas, table)

    def getCanvas(self):

        return self.__canvas

    def getMask(self):

        return self.__mask

    def getRois(self):

        return self.__rois

# test using a random image as the ooi and background
if __name__ == "__main__":

    start = time.time()
    ooi = cv2.imread("C:/Users/Andrew/Pictures/AILU.png")
    background_image = cv2.imread("F:/Data_aug_backgrounds/1573331342.2849042.png")
    canvas1 = Canvas(ooi, "C:/Users/Andrew/Documents/GitHub/AILU/examples/data/Image_resources_data_augmentation/canvas.png", "F:/Data_aug_backgrounds/1573331342.2849042.png")


    frame_with_background = modBackground.black_to_image(canvas1.getCanvas(), background_image)
    display.draw_and_show(frame_with_background, canvas1.getRois(), "canvas")

    if cv2.waitKey(25) & 0xFF == ord('q'):
        exit()
    end = time.time()
    total = end - start
    print("time:", total)
    time.sleep(10)
