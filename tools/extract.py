
import sys
sys.path.insert(1, '../.')
import ailu_python.image_processing.getROI as getROI
import cv2
from bounds import Bounds
import os
import numpy as np

def set_mask(event,x,y,_,hsv):

    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y, x]
        bounds.addColors(pixel)

    elif event == cv2.EVENT_RBUTTONDOWN:
        bounds.removeColors()

def pauseVideo():
    while True:
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break

def apply_mask(keeph, keepl, hsv):

    # blacks out everything except the values between keepl and keeph
    if not keepl is None:
        keep_mask = cv2.inRange(hsv, keepl, keeph)
        res = cv2.bitwise_and(hsv, hsv, mask=keep_mask)
        image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

        return image
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return image

def play_file(cap, filename, num, totalFile, path_to_bounds_file):

    precision = 10

    while cap.isOpened():
        ret, color_image = cap.read()
        if ret:
            color_image = cv2.resize(color_image,(960, 720))
            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)


            colorRange = bounds.getBounds()
            keeph = colorRange[0]
            keepl = colorRange[1]

            masked_image = hsv.copy()
            masked_image = apply_mask(keeph, keepl, masked_image)


            rois = getROI.using_color(masked_image)
            images = np.hstack((color_image, masked_image))

            cv2.setMouseCallback(filename + " " + str(num) + "/" + str(totalFile), set_mask, hsv)
            cv2.imshow(filename + " " + str(num) + "/" + str(totalFile), images)

            k = cv2.waitKey(33)
            if k == 112:
                pauseVideo()
            elif k == 115:
                bounds.saveBounds(path_to_bounds_file)
            elif k == 110:
                return True
            elif k == 98:
                return False
            elif k == 113:
                return None
            elif k == 121:
                bounds.increasePecision()
            elif k == 104:
                bounds.decreasePrecision()
        else:
            return True


bounds = Bounds()
path_to_file = "F:/data/weeds/RP-validation/"
path_to_bounds_file = "./extract_files/"
bounds_file = path_to_bounds_file + "bounds.npy"
file_list = os.listdir(path_to_file)
num = 0

while(True):

    filename = file_list[num]
    cap = cv2.VideoCapture(path_to_file+filename)
    ret = play_file(cap, filename, num + 1, len(file_list), path_to_bounds_file)

    if not ret is None:
        if ret == False:
            num = num - 1
            cv2.destroyAllWindows()
            if num < 0:
                num = len(file_list) - 1
                cv2.destroyAllWindows()
        else:
            num = num + 1
            cv2.destroyAllWindows()
            if num > len(file_list) - 1:
                num = 0
                cv2.destroyAllWindows()



    else:
        break

try:
    bounds = np.load(bounds_file)

except Exception as e:
    print(e)
    exit()

for filename in os.listdir(path_to_file):

    height = 600
    width = 800
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    fps = 30
    video_filename = output_path + str(time()) + 'output.avi'
    out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

    cap = cv2.VideoCapture(path_to_file+filename)

    while cap.isOpened():
        ret, color_image = cap.read()
        if not color_image is None:
            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
            keepl = np.asarray(bounds[0])
            keeph = np.asarray(bounds[1])
            keep_mask = cv2.inRange(hsv, keepl, keeph)
            res = cv2.bitwise_and(hsv, hsv, mask=keep_mask)
            image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

            rois = getROI.using_color(image)

            image = cv2.resize(image, (800,600))

            out.write(image)
            # display.draw_and_show(image, rois, "output")
        else:
            break;

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break










