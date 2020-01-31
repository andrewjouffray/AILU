import numpy as np

'''
Bounds is the object that handles and contains the upper a lower color bounds to keep in the image
'''

class Bounds:

    __pathToFiles = ""
    __listOfColors = []
    __bounds = [None,None]
    __lastBounds = [None, None]
    __precision = 10

    def __init__(self):
        pass

    # addColors will add colors that the user clicked on to the list of colors that have already been clicked on.
    def addColors(self, pixel):
        upper = [pixel[0] + self.__precision, pixel[1] + self.__precision, pixel[2] + self.__precision]
        lower = [pixel[0] - self.__precision, pixel[1] - self.__precision, pixel[2] - self.__precision]
        newColor = [upper, lower]
        self.__listOfColors.append(newColor)
        self.updateBounds()

    def removeColors(self):

        del self.__listOfColors[-1]
        self.__bounds = self.__lastBounds

    # this method looks at the list of all colors and keeps the highest and lowest values and sets them as keeph and keepl
    def updateBounds(self):

        # inits the value
        keepl = [0,0,0]
        keeph = [0,0,0]

        # checks if the list of color has been populated
        if len(self.__listOfColors) > 0:

            for color in self.__listOfColors:

                # finds the lowest values in mask_list and updates keepl
                if color[1][0] < keepl[0]:
                    keepl[0] = color[1][0]
                if color[1][1] < keepl[1]:
                    keepl[1] = color[1][1]
                if color[1][2] < keepl[2]:
                    keepl[2] = color[1][2]

                # finds the highest values in mask_list and updates keeph
                if color[0][0] > keeph[0]:
                    keeph[0] = color[0][0]
                if color[0][1] > keeph[1]:
                    keeph[1] = color[0][1]
                if color[0][2] > keeph[2]:
                    keeph[2] = color[0][2]


                # converts these values into
                keepl = np.asanyarray(keepl)
                keeph = np.asanyarray(keeph)

        self.__lastBounds = self.__bounds
        self.__bounds = [keeph, keepl]

    def getBounds(self):

        return self.__bounds

    def saveBounds(self, path):

        pathToSave = path + 'bounds'
        np.save(pathToSave, self.__bounds)
        print("> Saved bounds to", pathToSave + ".npy")

    def increasePecision(self):

        self.__precision -=1
        print("> precision margin: ", self.__precision)

    def decreasePrecision(self):

        self.__precision +=1
        print("> precision margin: ", self.__precision)