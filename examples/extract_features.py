import numpy as np
import cv2
import ailu_python.image_processing.getROI as getROI
import ailu_python.image_processing.getObject as getObject
import ailu_python.utils.display as display
from time import time
import os
import sys

if len(sys.argv) < 3:

    print("Missing arguments, source and destination e.g. python extract_features.py C:/myVidel.avi C:/data/training")
    exit()

path_to_file = sys.argv[1]
output_path = sys.argv[2]

# checks if the file exists
if not os.path.exists(path_to_file):
    print("could not find ", path_to_file)
    exit()
# checks if the out path exists creates on if not
if not os.path.exists(output_path):
    os.mkdir(output_path)
    print("created directory at: ", output_path)


height = 1080
width = 1920
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
fps = 30
video_filename = output_path + str(time()) + 'output.avi'
out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

for filename in os.listdir(path_to_file):

    cap = cv2.VideoCapture(filename)

    while cap.isOpened():
        ret, color_image = cap.read()

        #
        # color_image = cv2.resize(color_image, (640, 360))

        # blacked_color_img = getObject.using_blue(color_image)
        blacked_color_img = getObject.keep_green(color_image)

        rois = getROI.using_color(blacked_color_img)

        out.write(blacked_color_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()

