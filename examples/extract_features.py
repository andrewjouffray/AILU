import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display
from time import time
import os
import sys

if len(sys.argv) < 4:

    print("Missing arguments, source, destination, bounds e.g. python extract_features.py C:/myVidel.avi C:/data/training bounds.npy")
    exit()

path_to_file = sys.argv[1]
output_path = sys.argv[2]
bounds_file = sys.argv[3]

# checks if the file exists
if not os.path.exists(path_to_file):
    print("could not find ", path_to_file)
    exit()
# checks if the out path exists creates on if not
if not os.path.exists(output_path):
    os.mkdir(output_path)
    print("created directory at: ", output_path)

try:
    bounds = np.load(bounds_file)

except Exception as e:
    print(e)
    exit()

height = 1080
width = 1920
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
fps = 30
video_filename = output_path + str(time()) + 'output.avi'
out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

for filename in os.listdir(path_to_file):

    try:
        cap = cv2.VideoCapture(path_to_file+filename)

        while cap.isOpened():
            ret, color_image = cap.read()
            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
            keepl = np.asarray(bounds[0])
            keeph = np.asarray(bounds[1])
            keep_mask = cv2.inRange(hsv, keepl, keeph)
            res = cv2.bitwise_and(hsv, hsv, mask=keep_mask)
            image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

            rois = getROI.using_color(image)

            out.write(image)
            # display.draw_and_show(image, rois, "output")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



    except:
        print("pass")


