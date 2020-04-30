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
        # return true

    # calculates the exact value to set the motor speed to take the correct amount of images
    def getMotorSpeed(self, images, lowLimit):
        distanceToTravel = 396 - lowLimit
        speed = ((distanceToTravel*30) + (0.49 * images)) / (0.0097*images)
        return speed

    def getFromArduino(self, message):
        ser = serial.Serial("com3", 9600, timeout=0)
        message = message
        messageByte = message.encode()
        ser.write(messageByte)
        time.sleep(1)
        responce = ser.readline()
        responce = str(responce)
        responce = responce[2:-5]
        print(responce)
        return responce

    def comToArduinoWait(self, message):
        ser = serial.Serial("com3", 9600, timeout=0)
        message = message
        messageByte = message.encode()
        ser.write(messageByte)
        time.sleep(1)
        while true:
            responce = ser.readline()
            responce = str(responce)
            responce = responce[2:-5]
            if len(responce) > 0:
                print(responce)
                return responce

    def writeDatasetFile(self, datasetName, datasetType, bndBoxes, masks, workDir):
        files = os.listdir(workDir)
        label = []
        for file in files:
            if not "." in file:
                label.append(file)
        data = {'name':datasetName, 
        'type':datasetType, 
        'labels': label, 
        'outputType': [
            {'masks':masks,
            'boundingBoxes': bndBoxes
            }]
        }
        with open('dataset-config.json', 'w') as outfile:
            json.dump(data, outfile)


    def run(self):

        data = self.request.form
        dataSetName = data["dataSetName"]
        label = data["label"]
        images = int(data["images"])
        track = bool(data["track"])
        lowerLimit = int(data["lowerLimit"])
        rotateLimit = int(data["rotateLimit"])
        lights = int(data["lights"])
        datasetType = data["type"]
        bndBoxes = bool(data["bndBoxes"])
        masks = bool(data["bndBoxes"])

        if track:
            track = 1
        else:
            track = 0

        # setup paths
        workDir = "C:/Users/Andrew/Documents/GitHub/AILU/robot_controls/server/"+dataSetName+"/"
        saveDir = workDir+label

        #create a directory to save the rawData
        if not os.path.isdir(workDir):
            os.mkdir(workDir)

        #create a directory to save the rawData
        if not os.path.isdir(saveDir):
            os.mkdir(saveDir)

        speed = self.getMotorSpeed(images, lowerLimit)

        #position = getFromArduino("position")
        position = "bottom"

        if position == "top":
            direction = 0 #go down
        else:
            direction = 1 #go up

        #this is a dummy for the ser.write function
        print(speed, rotateLimit, track, lights, direction)

        self.writeDatasetFile(dataSetName, datasetType, bndBoxes, masks, workDir)

        self.recordAndSave(saveDir, images)
        
        return "done"



