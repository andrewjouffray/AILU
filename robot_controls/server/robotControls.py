import json
import os
import serial
import time
import threading
import cameraControls as cam

# calculates the exact value to set the motor speed to take the correct amount of images
def getMotorSpeed(images, lowLimit):
    distanceToTravel = 396 - lowLimit
    speed = ((distanceToTravel*30) + (0.49 * images)) / (0.0097*images)
    return speed

def getFromArduino(message):
    ser = serial.Serial("com6", 9600, timeout=0)
    messageByte = message.encode()
    ser.write(messageByte)
    time.sleep(1)
    responce = ser.readline()
    responce = str(responce)
    responce = responce[2:-5]
    return responce

def comToArduinoWait(message):
    ser = serial.Serial("com6", 9600, timeout=0)
    messageByte = message.encode()
    ser.write(messageByte)
    time.sleep(1)
    while true:
        responce = ser.readline()
        responce = str(responce)
        responce = responce[2:-5]
        if len(responce) > 0:
            return responce

def witeDatasetFile(datasetName, type, bndBoxes, masks, workDir):
    files = os.listdir(workDir)
    label = []
    for file in files:
        if not "." in file:
            label.append(file)
    data = {'name':datasetName, 'type':type, 'labels': label, 'outputType': [{'masks':masks, 'boundingBoxes': bndBoxes}]}
    with open('dataset-config.txt', 'w') as outfile:
        json.dump(data, outfile)


def runRobot(datasetName, label, images, track, lights, lowLimit, rotateLimit, type, bndBoxes, masks):

    # setup paths
    workDir = "C:/Users/andre/PycharmProjects/AILU_server/"+datasetName+"/"
    saveDir = workDir+"/"+label

    #create a directory to save the rawData
    if not os.path.isdir(saveDir):
        os.mkdir(saveDir)

    speed = getMotorSpeed(images, lowLimit)

    #position = getFromArduino("position")
    position = "bottom"

    if position == "top":
        direction = 0 #go down
    else:
        direction = 1 #go up

    videoCaptureThread = threading.Thread(target=cam.recordAndSave(), args=(saveDir, images))

    #this is a dummy for the ser.write function
    print(speed, rotateLimit, track, lights, direction)

    writeDatasetFile(datasetName, type, bndBoxes, masks, workDir)

    return "Imaging in progress"




