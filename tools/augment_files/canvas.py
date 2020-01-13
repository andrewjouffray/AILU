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
import random
import cv2
from ooi import Ooi
import time
sys.path.insert(1, '../.')
import ailu_python.data_augmentation.modify_background as modBackground
import ailu_python.utils.display as display

class Canvas:

    __width = 0
    __height = 0
    __aspectRatio = 0
    __listOfAspectRatios = [1.33, 1.66, 1.78, 1.85, 2.39]
    __objects = []
    __canvas = None
    __rois = []

    def __init__(self, ooi, pathToCanvas, background, maxOoi = 10):

        # gets a random image height, aspect ration and width
        self.__height = random.randint(360, 1080)
        self.__aspectRatio = self.__listOfAspectRatios[random.randint(0, len(self.__listOfAspectRatios) - 1)]
        self.__width = int(self.__height * self.__aspectRatio)
        self.__rois = []
        canvas = cv2.imread(pathToCanvas)

        # sets the canvas as the chosen background
        self.__canvas = canvas[:self.__height, :self.__width]

        # picks a random number of objects of interest to insert into the image
        numberOfOoi = random.randint(1, maxOoi)
        # print("number of ooi:", numberOfOoi)

        # divides the image into columns, one for each object of interest (ooi)
        columnWidth = int(self.__width / numberOfOoi)
        # print("column width:", columnWidth)

        # creates the objects of interest
        for i in range(numberOfOoi):

            # create a new object
            objectOfinterest = Ooi(ooi, columnWidth, self.__height, columnWidth * i)
            self.__objects.append(objectOfinterest)

            # gets it's position
            x1, y1, x2, y2 = objectOfinterest.getPosition()

            # inserts the object into the column
            try:
                self.__canvas[y1:y2, x1:x2] = objectOfinterest.getObject()
                self.__rois.append([x1, y1, x2, y2])
            except Exception as e:
                pass

        self.__canvas = modBackground.black_to_image(self.__canvas, background)

    def getCanvas(self):

        return self.__canvas

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