import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600)

time.sleep(2)
while 1:
    c="120"
    c=c.encode('utf-8')
    print(c)
    arduino.write(c)
    print("Hi python")
        #print(arduino.readline())
    time.sleep(4)