import ailu_python.utils.tmp as func
import random

class ObjectOfInterest:

    __image = []

    def __init__(self, image):

        rois_img = func.getAllRoiImage(image)
        largestRoi = rois_img[0]
        for roi in rois_img:
            if roi[0].any() > largestRoi:
                largestRoi = roi

        self.__image = largestRoi

    def randomlyModify(self):

        pass

    def scale(self, scale):

        # scale is a value between 0.1 and 2 typically
        self.__image = func.scale_image(self.__image, scale)

    def rotate(self, rotation):

        # between 0 and 360
        self.__image = func.rotate_image(self.__image, rotation)

    def blurr(self, kernelSize):

        # Kernel size between 1 and 15 usually
        self.__image = func.blurr(self.__image, kernelSize)

    def lowerResolution(self, denominator):

        # factor is how much you will divide the amount of pixels by usually between 2 and 10
        self.__image = func.lowerRes(self.__image, denominator)


