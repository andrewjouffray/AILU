'''
Extract is designed to allow users to read the video files, and remove the background.

Step 1:
play the video files and click on the pixels that you want to keep or remove in the image, then save the bounds

Step 2:
Process the videos

bounds = the color range of pixels to either keep or black out.

User Manual:
input directory: where the unprocessed .avi files are located
output directory: where the processed .avi files will go
keep foreground: answering "y" means that the pixels that you click will be kept, and the rest turned black,
answering "n" means that the pixels you click on will be turned black.

next video press: n
previous video press: b
save the bounds press: s
pause video: press p
quit / start processing video, press: q (press 's' before starting the processing of images, unless you want to quit)
lower precision, press: h (precision represent how many of the neighboring pixels will each click include )
increase precision: y

'''



import sys
sys.path.insert(1, '../.')

import cv2
from extract_files.bounds import Bounds
import os
import numpy as np
import time
import ctypes

# used later to get the screen size
user32 = ctypes.windll.user32

title1 = "\n   _____              .___            __________        __  .__                  ___________         __                        __   \n"
title2 = "  /  _  \   ____    __| _/______  ____\______   \ _____/  |_|__| ____   ______   \_   _____/__  ____/  |_____________    _____/  |_ \n"
title3 = " /  /_\  \ /    \  / __ |\_  __ \/  _ \|    |  _//  _ \   __\  |/ ___\ /  ___/    |    __)_\  \/  /\   __\_  __ \__  \ _/ ___\   __\n"
title4 = "/    |    \   |  \/ /_/ | |  | \(  <_> )    |   (  <_> )  | |  \  \___ \___ \     |        \>    <  |  |  |  | \// __ \\  \___|  |\n"
title5 = "\____|__  /___|  /\____ | |__|   \____/|______  /\____/|__| |__|\___  >____  >   /_______  /__/\_ \ |__|  |__|  (____  /\___  >__|\n"
title6 = "        \/     \/      \/                     \/                    \/     \/            \/      \/                  \/     \/      \n"
title = title1 + title2 + title3 + title4 + title5 + title6
print(title)
print(
    "=======================================================================================================================================================")
print(
    "=====================================================[enter \"exit\" at anytime to exit the program]=====================================================")


# checks the input directory to make sure valid file are in it
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


# adds or remove colors to the colors list when you click
def set_mask(event, x, y, _, parameters):

    hsv = parameters[0]
    bounds = parameters[1]

    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y, x]
        bounds.addColors(pixel)

    elif event == cv2.EVENT_RBUTTONDOWN:
        bounds.removeColors()


def pauseVideo():

    while True:
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break


# applies the color masks to the images before showing them to the user
def apply_mask(keeph, keepl, hsv, keepForeground):

    # blacks out everything except the values between keepl and keeph
    if not keepl is None:
        if keepForeground == True:
            keep_mask = cv2.inRange(hsv, keepl, keeph)
            res = cv2.bitwise_and(hsv, hsv, mask=keep_mask)
            image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

        else:
            keep_mask = cv2.inRange(hsv, keepl, keeph)
            hsv[keep_mask > 0] = ([0, 0, 0])
            image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        return image
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return image


# Displays the video file to the user, and allows him to brows through the videos and click on the pixels that
# the user wants to keep.
def play_file(cap, filename, num, totalFile, path_to_bounds_file, keepForeground, bounds):

    precision = 10
    while cap.isOpened():
        ret, color_image = cap.read()
        if ret:

            # gets the width and height of the user's screen
            Width = user32.GetSystemMetrics(0)
            Height = user32.GetSystemMetrics(1)

            # resize the image to fit in the user's screen
            color_image = cv2.resize(color_image, (int(Width/2), int(Height/2)))

            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            # gets the color range to keep or remove
            colorRange = bounds.getBounds()
            keeph = colorRange[0]
            keepl = colorRange[1]

            # apples the color mask to the image
            masked_image = hsv.copy()
            masked_image = apply_mask(keeph, keepl, masked_image, keepForeground)

            images = np.hstack((color_image, masked_image))

            # listens for a mouse click
            cv2.setMouseCallback(filename + " " + str(num) + "/" + str(totalFile), set_mask, [hsv, bounds])

            # shows the images
            cv2.imshow(filename + " " + str(num) + "/" + str(totalFile), images)

            k = cv2.waitKey(33)
            if k == 112: # p
                pauseVideo()
            elif k == 115: # s
                bounds.saveBounds(path_to_bounds_file)
            elif k == 110:
                return True
            elif k == 98:
                return False
            elif k == 113:
                return None
            elif k == 121: # y
                bounds.increasePecision()
            elif k == 104: # h
                bounds.decreasePrecision()
        else:
            return True


def getInputs():

    # gets input path
    while True:
        inputPath = input("\n> Enter Path to .avi files: ")
        if not inputPath.endswith("/"):
            inputPath = inputPath + "/"
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
            outPutPath = outPutPath + "/"
        if os.path.exists(outPutPath):
            break
        elif outPutPath.lower() == "exit":
            exit()
        else:
            os.mkdir(outPutPath)
            print("> Created path", outPutPath)
            break

    # gets the value dictating if clicks on the image will black out the pixels or keep the pixels
    while True:
        keepForegroundInput = input("\n> Keep foreground y/n: ")
        if keepForegroundInput.lower() == "y":
            keepForeground = True
            break
        else:
            keepForeground = False
            break


    return inputPath, videoFiles, outPutPath, keepForeground

def main():

    # creates bounds object
    bounds = Bounds()

    # paths to the bound file, the bounds file determines the range of colors to keep when processing the video files
    path_to_bounds_file = "./extract_files/"
    bounds_file = path_to_bounds_file + "bounds.npy"
    num = 0

    # remove the old bounds file
    try:
        os.remove(bounds_file)
    except:
        pass

    inputPath, videoFiles, outPutPath, keepForeground = getInputs()

    # =======================================================
    # PART 1: viewing the video files and defining the bounds
    # =======================================================
    while(True):

        # videoFiles is the list of video files contained in the input directory
        filename = videoFiles[num]

        # start video capture
        cap = cv2.VideoCapture(inputPath+filename)

        # starts displaying the video to the user, allowing them to select the color range to keep or remove
        ret = play_file(cap, filename, num + 1, len(videoFiles), path_to_bounds_file, keepForeground, bounds)

        # if the return value is not none, play the next video file or the previous video file
        if not ret is None:
            if ret == False:

                # plays the previous file
                num = num - 1
                cv2.destroyAllWindows()
                if num < 0:
                    num = len(videoFiles) - 1
                    cv2.destroyAllWindows()
            else:

                # plays the next file
                num = num + 1
                cv2.destroyAllWindows()
                if num > len(videoFiles) - 1:
                    num = 0
                    cv2.destroyAllWindows()


        # break and go to step 2
        else:
            break

    # =========================================================
    # PART 2: Processing the video files using the saved bounds
    # =========================================================

    # the bounds file should always be saved in the /extract_files/ folder
    try:
        bounds = np.load(bounds_file)

    except Exception as e:
        print("\n> No bounds file found. Exiting.")
        exit()

    # iterates over each video files in the input path
    for filename in os.listdir(inputPath):

        # defines the video recording and saving settings
        height = 1080
        width = 1920
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        fps = 30
        video_filename = outPutPath + str(time.time()) + 'output.avi'
        out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

        # start reading the video file
        cap = cv2.VideoCapture(inputPath+filename)
        print("\n> processing file", video_filename, "...")

        while cap.isOpened():

            # gets each frame in the video file
            ret, color_image = cap.read()
            if not color_image is None:

                # converts the image to HSV and gets the bounds
                hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
                keepl = np.asarray(bounds[1])
                keeph = np.asarray(bounds[0])

                # applies the mask on the image
                image = apply_mask(keeph, keepl, hsv, keepForeground)

                # saves the image
                out.write(image)

            else:
                break;

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    main()







