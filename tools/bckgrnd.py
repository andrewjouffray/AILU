import cv2
import sys
import os
import time

PATH_TO_CANVAS = "./augment_files/canvas.png"

title1 = "\n   _____              .___            __________        __  .__                __________                __                       .___\n"
title2 = "  /  _  \   ____    __| _/______  ____\______   \ _____/  |_|__| ____   ______ \______   \  ____   ____ |  | _________  ____    __| _/\n"
title3 = " /  /_\  \ /    \  / __ |\_  __ \/  _ \|    |  _//  _ \   __\  |/ ___\ /  ___/  |    |  _/ / ___\_/ ___\|  |/ /\_  __ \/    \  / __ | \n"
title4 = "/    |    \   |  \/ /_/ | |  | \(  <_> )    |   (  <_> )  | |  \  \___ \___ \   |    |   \/ /_/  >  \___|    <  |  | \/   |  \/ /_/ | \n"
title5 = "\____|__  /___|  /\____ | |__|   \____/|______  /\____/|__| |__|\___  >____  >  |______  /\___  / \___  >__|_ \ |__|  |___|  /\____ | \n"
title6 = "        \/     \/      \/                     \/                    \/     \/          \//_____/      \/     \/            \/      \/ \n"
title = title1 + title2 + title3 + title4 + title5 + title6
print(title)
print(
    "=======================================================================================================================================================")

# gets input path
print(
    "=====================================================[enter \"exit\" at anytime to exit the program]=====================================================")

# get inputs directory
source = input("\n> please enter to path to the source file: ")

out = input("\n> please enter to path to the destination folder: ")
# checks the given paths for the destination and source
if not os.listdir(out):
    # if the destination path doesn't exist, create one
    try:
        os.mkdir(out)

    except Exception as e:
        print(e)
        exit()

if not source.endswith("/"):
    source = source + "/"

if not out.endswith("/"):
    out = out + "/"

for file in os.listdir(source):

    # open video file
    cap = cv2.VideoCapture(source+file)
    count = 0
    while True:

        # Starts reading the file
        ret, frame = cap.read()
        if ret:
            count += 1

            # gets every 30 frames
            if count % 19 == 0:

                # creates a name and save the file
                name = str(time.time()) + ".png"
                cv2.imwrite(out+name, frame)
                print("successfully saved", int(count/30), "images", end="\r")
            else:
                pass
        else:
            break

print("done")
