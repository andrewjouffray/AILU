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
import random
import cv2
from ooi import Ooi
import time
import ailu_python.data_augmentation.modify_background as modBackground

class Canvas:

    __width = 0
    __height = 0
    __aspectRatio = 0
    __listOfAspectRatios = [1.33, 1.66, 1.78, 1.85, 2.39]
    __objects = []
    __canvas = None

    def __init__(self, ooi, pathToBackground, maxOoi = 10):

        self.__height = random.randint(360, 1080)
        self.__aspectRatio = self.__listOfAspectRatios[random.randint(0, len(self.__listOfAspectRatios) - 1)]
        self.__width = int(self.__height * self.__aspectRatio)

        print("height, width:", self.__height, self.__width)

        background = cv2.imread(pathToBackground)
        # cv2.imshow("background", background)

        self.__canvas = background[:self.__height, :self.__width]

        numberOfOoi = random.randint(1, maxOoi)
        print("number of ooi:", numberOfOoi)

        columnWidth = int(self.__width / numberOfOoi)
        print("column width:", columnWidth)

        # creates the objects of interest
        for i in range(numberOfOoi):
            print("created ooi.")
            objectOfinterest = Ooi(ooi, columnWidth, self.__height, columnWidth * i)
            self.__objects.append(objectOfinterest)
            x1, y1, x2, y2 = objectOfinterest.getPosition()

            self.__canvas[y1:y2, x1:x2] = objectOfinterest.getObject()

    def getCanvas(self):

        return self.__canvas

if __name__ == "__main__":

    start = time.time()
    ooi = cv2.imread("C:/Users/Andrew/Pictures/vid.png")
    background_image = cv2.imread("F:/Data_aug_backgrounds/1573331342.2849042.png")
    canvas1 = Canvas(ooi, "C:/Users/Andrew/Documents/GitHub/AILU/examples/data/Image_resources_data_augmentation/canvas.png")


    frame_with_background = modBackground.black_to_image(canvas1.getCanvas(), background_image)
    cv2.imshow("randomly generated canvas", frame_with_background)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        exit()
    end = time.time()
    total = end - start
    print("time:", total)
    time.sleep(10)