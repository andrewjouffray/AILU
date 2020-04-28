import cv2
import time
import asyncio


async def recordAndSave(savePath, Images):
    cap = cv2.VideoCapture("./rp-lighting-no-light.avi")
    frameNumber = 0
    name = savePath+"/data"+str(time.time())+"output.avi"
    out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (1920, 1080))
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frameNumber +=1
            out.write(frame)
            #save the frame or something
        else:
            break

        if frameNumber == Images:
            break

    cap.release()
    out.release()