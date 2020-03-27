import serial
import sys
sys.path.insert(1, '../examples')
from time import sleep
import keyboard  # using module keyboard


# make sure to check your com port
ser = serial.Serial("com6",9600, timeout=0)
sleep(2)


while True:  # making a loop

	keyboard.on_press_key("w", lambda _:ser.write(b'w200\n'))
			
	keyboard.on_press_key("s", lambda _:ser.write(b's200\n'))
		


	




