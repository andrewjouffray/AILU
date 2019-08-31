import serial
import bag_saver
from time import sleep

ser = serial.Serial("com3",9600, timeout=0)
# # string1 = "s50"
# ard.write(b's50')
sleep(2)
# while True:
# ser = serial.Serial()
# ser.baudrate = 9600
# ser.port = 'COM7' # write port on which you connected your Arduino
ser.write(b't\n')
ser.write(b'g\n')
sleep(60)
data = "o120\n"
bytesData = data.encode()
ser.write(bytesData)
data = "a355\n"
bytesData = data.encode()
ser.write(bytesData)

bag_saver.save_bag()

# ser.write(b'w100\n')
#
# ser.write(b'o90\n')
# ser.write(b'o85\n')
# ser.write(b'o120\n')
# ser.write(b'o95\n')

print('done')
ser.close()