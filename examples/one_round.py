import serial
import sys
import stream_and_save_color
from time import sleep

folder = "E:/AILU_RAW/weeds/CQL-validation/CQL-validation"

ser = serial.Serial("com3", 9600, timeout=0)
sleep(2)

data = "t\n"
bytesData = data.encode()
ser.write(bytesData)
sleep(22)


data = "s200\n"
bytesData = data.encode()
ser.write(bytesData)
sleep(27)


data = "o134\n"
bytesData = data.encode()
ser.write(bytesData)


data = "a355\n"
bytesData = data.encode()
ser.write(bytesData)

# start recording and saves the file as object_detection.bag
stream_and_save_color.get_video(folder)

data = "w100\n"
bytesData = data.encode()
ser.write(bytesData)
sleep(19)

data = "o144\n"
bytesData = data.encode()
ser.write(bytesData)

data = "t\n"
bytesData = data.encode()
ser.write(bytesData)

# start recording and saves the file as object_detection.bag
stream_and_save_color.get_video(folder)

data = "w100\n"
bytesData = data.encode()
ser.write(bytesData)
sleep(19)

data = "o152\n"
bytesData = data.encode()
ser.write(bytesData)

data = "a355\n"
bytesData = data.encode()
ser.write(bytesData)

stream_and_save_color.get_video(folder)