import serial
import sys
import stream_and_save
from time import sleep

ser = serial.Serial("com3", 9600, timeout=0)
sleep(2)
data = "o160\n"
bytesData = data.encode()
ser.write(bytesData)


data = "a355\n"
bytesData = data.encode()
ser.write(bytesData)

# start recording and saves the file as object_detection.bag
stream_and_save.get_video("E:/AILU_RAW/bad_milano/")

data = "s130\n"
bytesData = data.encode()
ser.write(bytesData)
sleep(19)

data = "o1\n"
bytesData = data.encode()
ser.write(bytesData)

data = "t\n"
bytesData = data.encode()
ser.write(bytesData)

# start recording and saves the file as object_detection.bag
stream_and_save.get_video("E:/AILU_RAW/bad_milano/")

data = "w130\n"
bytesData = data.encode()
ser.write(bytesData)
# sleep(12)