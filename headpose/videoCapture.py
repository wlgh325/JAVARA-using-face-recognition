
import numpy as np
import cv2
import argparse
import os.path as osp
# import serial
# import time
from hpd import HPD


def main(args):
    filename = args["input_file"]

    FACE_DOWNSAMPLE_RATIO = 2 #프레임 작게하기 **** 구현필요 ****
                              # ㄴ> cv2.resize() 활용
                              #참고링크:https://www.learnopencv.com/speeding-up-dlib-facial-landmark-detector/

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

    arduino = serial.Serial('/dev/ttyUSB0', 9600)

    count = 0

    # time.sleep(2)
    while(cap.isOpened()):
        # Capture frame-by-frame
        print('\rframe: %d' % count, end='')
        ret, frame = cap.read()

        # pretx = prety = pretz = '0.0'


        if isVideo:

            if (count % SKIP_FRAMES == 0):
                frame, angles, tvec = hpd.processImage(frame)
                print("\ntvec:\n {0}".format(tvec))
                tx, ty, tz = tvec[:, 0]
                print('getTvec tx: %s' % tx)
                print('getTvec ty: %s' % ty)
                print('getTvec tz: %s' % tz)
                rx, ry, rz = angles
                tx, ty, tz = tvec[:, 0]
            else:
                continue


            if frame is None:
                break
            else:

##                if (pretx == '0.0' and prety == '0.0' and
##                    pretz == '0.0'):
##
##                    pretx = tx
##                    prety = ty
##                    pretz = tz
##                else:
##                    arduino.write("rx")
##                    arduino.write(-rx)
##                    arduino.write("ry")
##                    arduino.write(-ry)
##                    arduino.write("rz")
##                    arduino.write(-rz)
##                    arduino.write("tx")
##                    arduino.write(tx-pretx)
##                    arduino.write("ty")
##                    arduino.write(ty-prety)
##                    arduino.write("tz")
##                    arduino.write(tz-pretz)
##
##                    time.sleep(0.1)
##
##                    pretx = tx
##                    prety = ty
##                    pretz = tz
##
                out.write(frame)


        else:
            frame = cv2.flip(frame, 1)
            frame, angles , tvec = hpd.processImage(frame)
##            frame, angles = hpd.processImage(frame)

            # Display the resulting frame
            cv2.imshow('frame',frame)
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
