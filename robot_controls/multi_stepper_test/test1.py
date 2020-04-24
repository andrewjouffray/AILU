import msvcrt
import serial
import sys
from time import sleep
from time import time
import keyboard  # using module keyboard



# make sure to check your com port
ser = serial.Serial("com6",9600, timeout=0)
sleep(2)

        

oldState = ''
pulses = 0
cycle  = 0
startTime = 1
startSpeed = 50
currentStateStripped = ""
print(str(ser.in_waiting))
ser.write(b'ready\n')
#sleep(5)


#currentState = ser.readline()
#print(str(currentState))
print("in " + str(ser.in_waiting))
print("out " + str(ser.out_waiting))
ser.write(b'test\n')
state = ''
while not state:
    state = ser.readline()
print(str(state))
state = ser.readline()
print(str(state))
state = ser.readline()
print(str(state))
state = ser.readline()
print(str(state))

    
#sleep(5)
#ser.write(b'z')

keyboard.add_hotkey('q', lambda: ser.write(b'q'))
keyboard.add_hotkey('z', lambda: ser.write(b'z'))
keyboard.add_hotkey('p', lambda: ser.write(b'300360131'))
# while True:

    # # TODO: add the calculate speed function
    # # add a way to allow sertain inputs to be sent over and others to only be sent once.
    
    # speed = startSpeed + (cycle * 50)
    
    # # read the current state 
    # print(str(ser.in_waiting))
    # currentState = ser.readline()
    # if currentState != b'' and str(currentState) != oldState:
        # stringCurrentState = str(currentState)
        # currentStateStripped = stringCurrentState[2:-5]
        # print(currentStateStripped)
        # oldState = stringCurrentState
        
    # if currentStateStripped == "top":
        # ser.write(b'300360132')
        # currentStateStripped = "going downx"

        
    # elif currentStateStripped == "bottom":
        # ser.write(b'300360131')
        # currentStateStripped = "going upx"

        
    # elif currentStateStripped == "zero complete":
        # ser.write(b'600360131')
        # currentStateStripped = "going upx"
        
    # elif currentStateStripped == "going up":
        # pass
        
    # elif currentStateStripped == "going down":
        # pass
        
        
    # if keyboard.read_key() == "w":
        # ser.write(b'w')
        
    # elif keyboard.read_key() == "s":
        # ser.write(b's')







