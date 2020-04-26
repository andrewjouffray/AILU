import cv2
import time


def recordAndSave(savePath, Images):
    cap = cv2.VideoCapture(0);
    frameNumber = 0;
    while cap.isOpen():
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        name = savePath+"/"+str(time.time())+"output.py"
        out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
        ret, frame = cap.read()
        if ret:
            frameNumber +=1;
            out.write(frame)
            #save the frame or something
            if frameNumber == Images:
                break