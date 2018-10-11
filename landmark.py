import time
from picamera import PiCamera
import os
from picamera.array import PiRGBArray
import cv2
import sys
import dlib
import glob

camera = PiCamera(resolution=(680,480))
camera.start_preview()
shutter_speed=0.1
initial_time = 5
total_capture_time=10
time.sleep(1)

for filename in camera.capture_continuous('./image/frame.jpg'):
    print(filename)
    time.sleep(shutter_speed)
    print("remove")
    os.remove(filename)
    print('frame.jpg remove)
    key = cv2.waitKey(1) & 0xFF
    cv2.imshow("Frame",camera);
    if key == ord("q"):
        break
camera.stop_preview()
camera.close()

def landmarkDetection(predictor):
    predictor_path = '/shape_predictor_68_face_landmarks (1).dat.bz2'
    faces_folder_path = '/image/'

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    win = dlib.image_window()

    for f in glob.glob(os.path.join(faces_folder_path, "frame.jpg")):
        print("Processing file: {}".format(f))
        img = dlib.load_rgb_image(f)

        win.clear_overlay()
        win.set_image(img)

        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.
        dets = detector(img, 1)
        print("Number of faces detected: {}".format(len(dets)))
        for k, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                k, d.left(), d.top(), d.right(), d.bottom()))
            # Get the landmarks/parts for the face in box d.
            shape = predictor(img, d)
            print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
                                                      shape.part(1)))
            # Draw the face landmarks on the screen.
            win.add_overlay(shape)

        win.add_overlay(dets)
        dlib.hit_enter_to_continue()

