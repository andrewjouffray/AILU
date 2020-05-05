import serial
from time import sleep

# open the serial communication, (<port>, <baudrate>, <timeout>)
ser = serial.Serial("com7",9600, timeout=0)

sleep(2)

# zero the horizontal axis
ser.write(b't\n')

# zero the vertical axis
ser.write(b'g\n')

# wait for 1 minute for the vertical axis to lower itself
# this is one of the problems, I have to hard-code the amount of time to wait before sending another command,
# rather that waiting for the Arduino to tell me it's done.
sleep(60)

# This is a simple loop that moves one step clock-wise and then moves 350 steps vertically (one vertical step per second)
# I actually would rather have it move one step vertically and pan across horizontally
for i in range(1, 355):
    data = "a1\n" # command to be sent (move 1 step horizontally)
    bytesData = data.encode() # encode command into bytes
    ser.write(bytesData) # send the command to the arduino
    sleep(1) #wait one second
    for j in range(1, 350):
        data = "w0\n" # command to be sent (move 1 step vertically)
        bytesData = data.encode()
        print(j)
        ser.write(bytesData)
        sleep(1)
        print("photo")

    # when the camera has reached the top, zero the vertical axis
    ser.write(b'g\n')

    # wait 1 minute for the camera to go all the way down
    sleep(60)


print('done')
ser.close()