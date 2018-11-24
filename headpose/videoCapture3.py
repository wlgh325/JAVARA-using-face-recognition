import numpy as np
import cv2
import argparse
import os.path as osp
import serial
import time
from hpd import HPD


default_servoAngle = 90
default_xAngle = 60
def main(args):
    filename = args["input_file"]

    RESIZE_RATIO = 2.45 #프레임 작게하기
    SKIP_FRAMES = 3 #프레임 건너뛰기: 3프레임마다 영상처리
                    #테스트하며 값 조정 필요

    if filename is None:
        isVideo = False
        cap = cv2.VideoCapture(-1)
        cap.set(3, 640)
        cap.set(4, 480)

    else:
        isVideo = True
        cap = cv2.VideoCapture(filename)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        name, ext = osp.splitext(filename)
        out = cv2.VideoWriter(args["output_file"], fourcc, fps, (width, height))

    # Initialize head pose detection
    hpd = HPD(args["landmark_type"], args["landmark_predictor"])

    xy_arduino = serial.Serial('/dev/ttyUSB0', 9600)
    #servo_arduino = serial.Serial('/dev/ttyACM2',9600)
    #z_arduino = serial.Serial('/dev/ttyACM0', 9600)
    
    # servo motor default angle
    servo_angle = default_servoAngle
    tempAngle = str(servo_angle)
    tempAngle = tempAngle.encode('utf-8')
    #servo_arduino.write(tempAngle)
    
    count = 0

    cv2.namedWindow('frame2', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame2', 320, 240)

    # time.sleep(2)
    while(cap.isOpened()):
        # Capture frame-by-frame
        print('\rframe: %d' % count, end='')
        ret, frame = cap.read()

        h, w, c = frame.shape
        new_h = (int)(h / RESIZE_RATIO)
        new_w = (int)(w / RESIZE_RATIO)
        frame_small = cv2.resize(frame, (new_w, new_h))
        frame_small2 = cv2.flip(frame_small, 1) # 좌우반전: 카메라 거울상
        frame_small3 = cv2.flip(frame_small, 0) # 상하반전

        pretx = prety = pretz = '0.0'
        tx = ty = tz = '0.0'

        if isVideo:

            if frame is None:
                break
            else:
                out.write(frame)

        else:
##            //cv2.imshow('frame3',frame_small3)

            if (count % SKIP_FRAMES == 0):               
                frameOut, angles, tvec = hpd.processImage(frame_small3)
                if tvec==None:
                    print('\rframe2: %d' % count, end='')        
                    print(" There is no face detected\n")
                    count += 1
                    continue
                    
                else:
                    tx, ty, tz = tvec[:, 0]
                    rx, ry, rz = angles
                    ry = round(ry)
                    servo_angle = servo_angle + ry
                    tempAngle = str(servo_angle)
                    tempAngle = tempAngle.encode('utf-8')
                    
                    y_angle = str(int(ry) )
                    y_angle = y_angle.encode('utf-8')
                    
                    print("\ntx: ",tx, "\nty: ", ty,"\ntz: ", tz)
                    
                    #xy_arduino.write(X)
                    #xy_arduino.write(tz)
                    #xy_arduino.write(Y)
                    
                    temp_x = int(tx)
                    temp_x = str(temp_x)
                    print("\n\n\nstr_tx: ", temp_x)
                    temp_x = temp_x.encode('utf-8')
                    
                    
                    temp_z = int(tz) + default_xAngle
                    temp_z = str(temp_z)
                    print("\n\n\nstr_tx: ", temp_z)
                    temp_z = temp_z.encode('utf-8')
                    
                    #y 축돌리기
                    xy_arduino.write(temp_x)
                    
                    #xy_arduino.write(y_angle) #x 축돌리
                    # servo_arduino.write(tempAngle)
                    #z_arduino.write(y_angle)
                    time.sleep(0.5)
            
            else:
                count += 1
                pass


            if (pretx == '0.0' and prety == '0.0' and pretz == '0.0'):
                pretx = tx
                prety = ty
                pretz = tz
            else:
                pretx = tx
                prety = ty
                pretz = tz
            # Display the resulting frame
            cv2.imshow('frame2',frameOut)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        count += 1

    # When everything done, release the capture
    cap.release()
    if isVideo: out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', metavar='FILE', dest='input_file', default=None, help='Input video. If not given, web camera will be used.')
    parser.add_argument('-o', metavar='FILE', dest='output_file', default=None, help='Output video.')
    parser.add_argument('-lt', metavar='N', dest='landmark_type', type=int, default=1, help='Landmark type.')
    parser.add_argument('-lp', metavar='FILE', dest='landmark_predictor',
                        default='model/shape_predictor_68_face_landmarks.dat', help="Landmark predictor data file.")
    args = vars(parser.parse_args())
    main(args)
