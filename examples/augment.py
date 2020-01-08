'''
     _             _             ___       _   _              _                                    _
    /_\  _ __   __| |_ __ ___   / __\ ___ | |_(_) ___ ___    /_\  _   _  __ _ _ __ ___   ___ _ __ | |_ ___ _ __
  //_\\| '_ \ / _` | '__/ _ \ /__\/// _ \| __| |/ __/ __|  //_\\| | | |/ _` | '_ ` _ \ / _ \ '_ \| __/ _ \ '__|
/  _  \ | | | (_| | | | (_) / \/  \ (_) | |_| | (__\__ \ /  _  \ |_| | (_| | | | | | |  __/ | | | ||  __/ |
\_/ \_/_| |_|\__,_|_|  \___/\_____/\___/ \__|_|\___|___/ \_/ \_/\__,_|\__, |_| |_| |_|\___|_| |_|\__\___|_|
                                                                      |___/

This is the main file

input: directory containing processed video files from the robot, output directory.

step1: load the video file
step2: for each frame in the video, get the object of interest
step3: create a specified number of canvases with this object
step4: save those canvases in a specified folder along with data about the objects in a separate XML file
step5: repeat until there are no more video files

output: Large number of random training data

'''

import os
import sys
sys.path.insert(1, '../.')
import time
import ailu_python.utils.tmp as func
import cv2
from canvas import Canvas
import Workers
import random
import ailu_python.utils.display as display

def loadBackgrounds(path):
    try:
        print("> Loading background images...")
        files = os.listdir(path)
        validFiles = []
        print("> Checking files...")
        for file in files:
            if file.endswith(".png"):
                validFiles.append(path + file)
        if len(validFiles) == 0:
            raise Exception("no valid files in directory")
        print("> Background successfully loaded", len(validFiles), "images")
    except Exception as e:
        print("> Failed to load background images")
        print("> Error:", e)
        return False

    return validFiles

def loadInput(path):
    try:
        print("> Loading input videos files...")
        files = os.listdir(path)
        validFiles = []
        print("> Checking files...")
        for file in files:
            if file.endswith(".avi"):
                validFiles.append(file)
        if len(validFiles) == 0:
            raise Exception("no valid files in directory")
        print("> Background successfully loaded", len(validFiles), "videos files")
    except Exception as e:
        print("> Failed to load videos files")
        print("> Error:", e)
        return False

    return validFiles

# TODO: make it so that it can use more that 1 roi
def getOoi(frame):
    rois_img = func.getAllRoiImage(frame)
    if rois_img[0] is None:
        print("> Error: rois[0] is None")
        return False
    if rois_img[0].any() < 1 and len(rois_img) > 2:
        rois_img[0] = rois_img[1]
    elif rois_img[0].any() < 1:
        print("> Error: no roi in the frame")
        return False
    return rois_img[0]

def getRandomBackground(backgrounds):

    background_image_filename = backgrounds[random.randint(0, len(backgrounds) - 1)]
    background_image = cv2.imread(background_image_filename)

    while background_image is None:
        background_image_filename = backgrounds[random.randint(0, len(backgrounds) - 1)]
        background_image = cv2.imread(background_image_filename)

    return background_image


def main():

    PATH_TO_CANVAS = "./data/Image_resources_data_augmentation/canvas.png"

    title1 ="\n     _____              .___            __________        __  .__                   _____                                      __      \n"
    title2 ="    /  _  \   ____    __| _/______  ____\______   \ _____/  |_|__| ____   ______   /  _  \  __ __  ____   _____   ____   _____/  |_  ___________  \n"
    title3 ="   /  /_\  \ /    \  / __ |\_  __ \/  _ \|    |  _//  _ \   __\  |/ ___\ /  ___/  /  /_\  \|  |  \/ ___\ /     \_/ __ \ /    \   __\/ __ \_  __ \ \n"
    title4 ="  /    |    \   |  \/ /_/ | |  | \(  <_> )    |   (  <_> )  | |  \  \___ \___ \  /    |    \  |  / /_/  >  Y Y  \  ___/|   |  \  | \  ___/|  | \/ \n"
    title5 ="  \____|__  /___|  /\____ | |__|   \____/|______  /\____/|__| |__|\___  >____  > \____|__  /____/\___  /|__|_|  /\___  >___|  /__|  \___  >__|    \n"
    title6 ="          \/     \/      \/                     \/                    \/     \/          \/     /_____/       \/     \/     \/          \/        \n"
    title = title1 + title2 + title3 + title4 + title5 + title6
    print(title)
    print("=======================================================================================================================================================")

    # gets input path
    print("=====================================================[enter \"exit\" at anytime to exit the program]=====================================================")
    while True:
        inputPath = input("\n> Enter Path to .avi files: ")
        if not inputPath.endswith("/"):
            inputPath = inputPath+"/"
        if os.path.exists(inputPath):
            videoFiles = loadInput(inputPath)
            if videoFiles:
                break
        elif inputPath.lower() == "exit":
            exit()
        else:
            print("> Error: path not found", inputPath)

    # gets output path
    while True:
        outPutPath = input("\n> Enter Output Path: ")
        if not outPutPath.endswith("/"):
            outPutPath = outPutPath+"/"
        if os.path.exists(outPutPath):
            break
        elif outPutPath.lower() == "exit":
            exit()
        else:
            os.mkdir(outPutPath)
            print("> Created path", outPutPath)
            break

    # gets the path to the background images
    while True:
        backgroundPath = input("\n> Enter Path to Background images: ")
        if not backgroundPath.endswith("/"):
            backgroundPath = backgroundPath+"/"
        if os.path.exists(backgroundPath):
            backgrounds = loadBackgrounds(backgroundPath)
            if backgrounds:
                break
        elif backgroundPath.lower() == "exit":
            exit()
        else:
            print("> Error: path not found", backgroundPath)

    label = input("\n> Enter the label of the objects: ")

    while True:
        numberOfCanvases = input("\n> Multiply image by (1 -10): ")
        if numberOfCanvases.isnumeric():
            numberOfCanvases = int(numberOfCanvases)
            if numberOfCanvases >= 1 and numberOfCanvases <= 10:
                break
            else:
                print("> Error: enter a number between 1 - 10", backgroundPath)
        elif backgroundPath.lower() == "exit":
            exit()
        else:
            print("> Error: enter a number between 1 - 10", backgroundPath)

    imageCount = 0
    addedTotal = 0
    for file in videoFiles:
        print("\n\n=======================================================================================================================================================")
        print("\n> Processing file:", file)
        cap = cv2.VideoCapture(inputPath+file)

        while cap.isOpened():


            ret, frame = cap.read()
            if ret == True:
                ooi = getOoi(frame)
                if not type(ooi)==bool:
                    for i in range(numberOfCanvases):
                        imageCount += 1
                        start = time.time()


                        canvas1 = Canvas(ooi,PATH_TO_CANVAS,getRandomBackground(backgrounds))

                        # creates a 1/3 chance to get a lower res image and a 1/10 chance to get a blurry image
                        if random.randint(1, 3) == 1:
                            image = func.lowerRes(canvas1.getCanvas(), random.randint(1, 2.5))
                        else:
                            if random.randint(1, 10) == 1:
                                image = func.blurr(canvas1.getCanvas(), 7)
                            else:
                                image = canvas1.getCanvas()

                        # randomly darkens or lightens a third of the images
                        if random.randint(1, 3) == 1:
                            image = func.adjust_gamma(image, round(random.uniform(0.7, 2.5), 1))

                        Workers.save_images(image, canvas1.getRois(), outPutPath, label)

                        end = time.time()
                        total = end - start
                        addedTotal = addedTotal + total
                        average = addedTotal / imageCount
                        print(str(imageCount) + " / "+ str(630 * len(videoFiles) * numberOfCanvases) +" images generated | " + str(round(total, 5)) + " seconds per images | average: " + str(round(average, 5)) + " seconds.", end="\r")

                        # Uncomment to see what the images look like

                        # display.draw_and_show(image, canvas1.getRois(), "canvas")
                        # if cv2.waitKey(25) & 0xFF == ord('q'):
                        #     print("\n> Exiting...")
                        #     exit()
                        # time.sleep(2)
            else:
                break



if __name__ == "__main__":
    main()







