import serial 
from time import sleep
import cv2

ser = serial.Serial("COM3", 9600, timeout=.1)
sleep(2)

def send(message):
    message = message+"\n"
    messageByte = message.encode()
    ser.write(messageByte)

def getFromArduino(message):
    while True:
        responce = ser.readline()
        responce = responce.decode()
        responce = responce.rstrip()
        send(message)
        if len(responce) > 0:
            print(responce)
            return responce


# getFromArduino("this is my message")


def stream(Images):
    cap = cv2.VideoCapture("./rp-lighting-no-light.avi")
    frameNumber = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frameNumber +=1
            cv2.imshow('AILU_feed', frame)
            try:
                if (cv2.waitKey(1) & 0xFF == ord('q')) or frameNumber == Images:
                    break

            except Exception:
                print(Exception)
            

    try:
        cap.release()
        cv2.destroyWindow('AILU_feed') 

    except Exception:
        print(Exception)

stream(600)