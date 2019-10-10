import serial
import sys
import stream_and_save
from time import sleep

ser = serial.Serial("com3", 9600, timeout=0)
sleep(2)
option = "1"
data = "o155\n"
bytesData = data.encode()
ser.write(bytesData)

if option == "1":

    data = "a355\n"
    bytesData = data.encode()
    ser.write(bytesData)

    # start recording and saves the file as object_detection.bag
    stream_and_save.get_video("F:/AILU_RAW/bad_milano/")
    sleep(1)
else:


    data = "t\n"
    bytesData = data.encode()
    ser.write(bytesData)

    # start recording and saves the file as object_detection.bag
    stream_and_save.get_video("F:/AILU_RAW/bad_milano/")
    sleep(1)