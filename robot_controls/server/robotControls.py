import json
import os
import serial
import time
import threading
import cv2
import asyncio
from threading import Thread

class Compute(Thread):

    request = ''

    def __init__(self, request):
        Thread.__init__(self)
        self.request = request

    def recordAndSave(self, savePath, Images):
        cap = cv2.VideoCapture(0)
        frameNumber = 0
        name = savePath+"/data"+str(time.time())+"output.avi"
        out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 25, (1920, 1080))
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frameNumber +=1
                out.write(frame)
                if frameNumber == Images:
                    cap.release()
                    out.release()
                    exit()
                #save the frame or something
            else:
                break

        exit()


        # return true

    def stream(self, Images):
        # we use this video to simulate the camera stream
        cap = cv2.VideoCapture(0)
        frameNumber = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frameNumber +=1
                cv2.imshow('AILU_feed', frame)
                try:
                    # the video file we use, only has 630 frames so we limit it manually
                    if (cv2.waitKey(1) & 0xFF == ord('q')) or frameNumber == 1000:
                        cap.release()
                        cv2.destroyWindow('AILU_feed')
                        exit()

                except Exception:
                    print(Exception)

        try:
            cap.release()
            cv2.destroyWindow('AILU_feed')

        except Exception:
            print(Exception)

        exit()


    def run(self):

        data = self.request

        if data[0] == "stream":
            self.stream(data[2])
        else:
            self.recordAndSave(data[1], data[2])

            return "done"
