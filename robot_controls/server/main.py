from flask import Flask
from flask import request
from robotControls import Compute
import serial
import time 
import json
import robotControls as robot
import os

ROBOT_NAME = "AILU_0001"

com = "COM3"
app = Flask(__name__)
ser = serial.Serial(com, 9600, timeout=.1)
time.sleep(2)

def send(message):
    message = message+"\n"
    messageByte = message.encode()
    ser.write(messageByte)

def flush():
    while ser.readline():
        responce = ser.readline()
        pass

def comToArduino(message):
    send(message)
    while True:
        responce = ser.readline()
        responce = responce.decode()
        responce = responce.rstrip()
        if len(responce) > 0:
            print(responce)
            flush()
            return responce

def getMotorSpeed(images, lowLimit):
    distanceToTravel = 396 - lowLimit
    speed = ((distanceToTravel*30) + (0.49 * images)) / (0.0097*images)
    return int(speed)


def writeDatasetFile(datasetName, datasetType, bndBoxes, masks, workDir):
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

@app.route('/run', methods = ['POST'])
def run():

    data = json.loads(request.data.decode())

    # handles quick checks
    if data["runType"] == "test":

        images = int(data["images"])
        position = comToArduino("getPosition")
        print("position from arduino: ", position)

        if position == "top":
            command = "runD" #go down
        else:
            command = "runU" #go up

        # constamt speed for quick checks
        speed = "2000"

        command = command+speed
        comToArduino(command)

        imagingConfig = ["stream", "none", images]

        # starts imaging
        thread_a = Compute(imagingConfig)
        thread_a.start()

        responce = {"message":"quick check in progress"}
        return responce, 201
    else:

        dataSetName = data["dataSetName"]
        label = data["label"]
        images = int(data["images"])
        track = bool(data["track"])
        lights = int(data["lights"])
        datasetType = data["type"]
        bndBoxes = bool(data["bndBoxes"])
        masks = bool(data["masks"])
        lowerLimit = int(data["lowerLimit"])

        workDir = "C:/Users/Andrew/Documents/GitHub/AILU/robot_controls/server/"+dataSetName+"/"
        saveDir = workDir+label

        #create a directory to save the rawData
        if not os.path.isdir(workDir):
            os.mkdir(workDir)

        #create a directory to save the rawData
        if not os.path.isdir(saveDir):
            os.mkdir(saveDir)

        speed = getMotorSpeed(images, lowerLimit)

        position = comToArduino("getPosition")
        print("position from arduino: ", position)

        if position == "top":
            command = "runD" #go down
        else:
            command = "runU" #go up

        imagingConfig = ["save", saveDir, images]

        # starts imaging
        thread_a = Compute(imagingConfig)
        thread_a.start()

        # writes the command to the arduino
        command = command+str(speed)
        comToArduino(command)

        # writes the dataset config file
        writeDatasetFile(dataSetName, datasetType, bndBoxes, masks, workDir)

        responce = {"message":"imaging in progress"}
        return responce, 201

@app.route('/set', methods = ['POST'])
def setSettings():
    data = json.loads(request.data.decode())

    command = data["command"]
    value = data["value"]
    message = comToArduino(command+value)
    responce = {"message":message}
    return responce, 201

@app.route('/get', methods = ['GET'])
def getSettings():
    message = comToArduino("getSettings")
    messageList = message.split(",")
    print(messageList)
    responce = {"Vspeed":messageList[0], "Vlimit": messageList[1], "Hlimit": messageList[2], "tracking": messageList[3], "lighting":messageList[4]}
    return responce, 201

@app.route('/status', methods = ['GET'])
def getStatus():
    responce = {"message":"ready"}
    return responce, 201

app.run()