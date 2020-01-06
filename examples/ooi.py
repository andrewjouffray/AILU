"""
Ooi stands of Objects of interest, those are the objects that are added to the background image (canvas)

The canvas creates between 1 - 10 ooi and needs to place them on the image without overlapping between ooi. So
the algorithm defines a column on the canvas for each of those objects to be passed in. the left boundary of these
columns are the xAbsolutePos. The vertical boundary is the top of the image therefor yAbsolutePos always starts at 0

setp1: rotate
step2: scale
step3: position

"""
import numpy as np
import cv2
import random

class Ooi:
    __heightOfOoi = 0
    __widthOfOoi = 0
    __xAbsolutePos = 0
    __yAbsolutePos = 0
    __image = None
    __maxScale = 0
    __minScale = 0.08

    def __init__(self, objectOfInterest, columWidth, columnHeight, xAbsolutePos):

        self.__image = objectOfInterest

        # rotate the object
        angle = random.randint(0, 360)
        self.rotate(angle)


        # scale the object
        height, width = self.__image.shape[:2]
        maxScaleHeight = (columnHeight / height) - 0.1
        maxScaleWidth = (columWidth / width) - 0.1

        # find the maximum scale for the object to fit in the column
        if maxScaleHeight > maxScaleWidth:
            self.__maxScale = maxScaleWidth
        else:
            self.__maxScale = maxScaleHeight


        scale = random.uniform(self.__minScale, self.__maxScale)
        self.scale(scale)

        try:
        # define the position of the object on the canvas within given boundaries
            height, width = self.__image.shape[:2]
            maxXOffSet = columWidth - width
            maxYOffSet = columnHeight - height
            xOffSet = random.randint(0, maxXOffSet)
            yOffSet = random.randint(0, maxYOffSet)
        except Exception as e:
            print("error: ", e)
            print("height, width of the object: ", height, width)
            print("maxXOffSet value:", maxXOffSet)
            if maxYOffSet:
                print("maxYOffSet value:", maxYOffSet)


        #set the X1 Y1 positions
        self.__xAbsolutePos = xAbsolutePos + xOffSet
        self.__yAbsolutePos = yOffSet

        # set the X2 Y2 positions
        self.__widthOfOoi = self.__xAbsolutePos + width
        self.__heightOfOoi = self.__yAbsolutePos + height



    def rotate(self, degree):
        height, width = self.__image.shape[:2]
        image_center = (width / 2, height / 2)

        rotation_mat = cv2.getRotationMatrix2D(image_center, degree, 1.)

        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        rotated_mat = cv2.warpAffine(self.__image, rotation_mat, (bound_w, bound_h))

        self.__image = rotated_mat


    def scale(self, size):
        height, width = self.__image.shape[:2]
        image_center = (width / 2, height / 2)

        rotation_mat = cv2.getRotationMatrix2D(image_center, 1., size)

        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        rotated_mat = cv2.warpAffine(self.__image, rotation_mat, (bound_w, bound_h))

        self.__image = rotated_mat

    def getPosition(self):
        return self.__xAbsolutePos, self.__yAbsolutePos, self.__widthOfOoi, self.__heightOfOoi

    def getObject(self):
        return self.__image
