import serial
import time

arduino = serial.Serial('COM4', 9600)

while 1:
    c="360"
    c=c.encode('utf-8')
    print(c)
    arduino.write(c)
    print("Hi python")
        #print(arduino.readline())
    time.sleep(4)