import serial
import time

xy_arduino = serial.Serial('/dev/ttyUSB0', 9600)
#z_arduino = serial.Serial('/dev/ttyACM0', 9600)
#servo_arduino = serial.Serial('/dev/ttyACM1', 9600)

#time.sleep(1)
x_angle="-90"
y_angle="-90"
z_angle = "-10"
servo_angle ="-120"
delimiter = "/"

xy_angle = x_angle + delimiter + y_angle

xy_angle = xy_angle.encode('utf-8')
z_angle = z_angle.encode('utf-8')
servo_angle = servo_angle.encode('utf-8')

xy_arduino.write(xy_angle)

#z_arduino.write(z_angle)
#servo_arduino.write(servo_angle)