import serial
import sys
sys.path.insert(1, '../examples')
import stream_and_save
from time import sleep


# make sure to check your com port
ser = serial.Serial("com3",9600, timeout=0)
sleep(2)

# zero the rotation axis
ser.write(b't\n')

#zero the z axis
ser.write(b'g\n')

# wait for the z axis to go all the way down
sleep(60)
# pitch the camera 120 degrees (0 degrees is vertical looking up)
data = "o120\n"
bytesData = data.encode()
ser.write(bytesData)

for i in range(5):
    # rotate all the way around the object
    data = "a355\n"
    bytesData = data.encode()
    ser.write(bytesData)

    # start recording and saves the file as object_detection.bag
    stream_and_save.get_video("F:/AILU_RAW/bad_milano/")
    sleep(1)

    # Move up 30 mm
    data = "w30\n"
    bytesData = data.encode()
    ser.write(bytesData)
    sleep(2)

    ser.write(b't\n')
    stream_and_save.get_video("F:/AILU_RAW/bad_milano/")

    sleep(1)

    # Move up 30 mm
    data = "w30\n"
    bytesData = data.encode()
    ser.write(bytesData)
    sleep(2)

    print('done')
