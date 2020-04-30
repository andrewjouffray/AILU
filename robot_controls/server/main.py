from flask import Flask
from flask import request
from robotControls import Compute
import serial
import time 

import robotControls as robot

app = Flask(__name__)


def getFromArduino(message):
    ser = serial.Serial("com3", 9600, timeout=0)
    message = message
    messageByte = message.encode()
    ser.write(messageByte)
    time.sleep(1)
    responce = ser.readline()
    responce = str(responce)
    print(responce)
    responce = responce[2:-5]
    ser.close()
    return responce

def comToArduinoWait(message):
    ser = serial.Serial("com3", 9600, timeout=0)
    messageByte = message.encode()
    ser.write(messageByte)
    time.sleep(1)
    while True:
        responce = ser.readline()
        responce = responce.decode()
        responce = responce.rstrip()
        if len(responce) > 0:
            print(responce)
            ser.close()
            return responce

    

@app.route('/run', methods = ['POST'])
def run():
    
    thread_a = Compute(request.__copy__())
    thread_a.start()
    return "Processing in background", 200

@app.route('/get', methods = ['GET'])
def getSettings():
    message = getFromArduino("g")
    
    return message, 200


@app.route('/set', methods = ['POST'])
def setSettings():
    value = request.form["setting"]
    print(value)
    message = getFromArduino("s"+value)
    return message, 200

@app.route('/longGet', methods = ['POST'])
def longGetSettings():
    message = comToArduinoWait("m")
    return message, 200

app.run()