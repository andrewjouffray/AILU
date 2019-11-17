import cv2
import sys
import os
import time

# get inputs and check if they are there
input_args = sys.argv

if input_args[1]:
    source = input_args[1]
else:
    print("please enter to path to the source file")

if input_args[2]:
    destination = input_args[2]
else:
    print("please enter to path to the destination folder")


# checks the given paths for the destination and source
if not os.listdir(destination):
    # if the destination path doesn't exist, create one
    try:
        os.mkdir(destination)

    except Exception as e:
        print(e)
        exit()

# open video file
try:
    cap = cv2.VideoCapture(source)
except Exception as e:
    print(e)
    exit()

count = 0
while cap.isOpened():

    ret, frame =cap.read()
    # creates a name and save the file
    name = "/" + str(time.time()) + ".png"
    cv2.imwrite(destination+name, frame)
    count += 1
    print("successfully saved", count, "images")

print("done")
