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


while True:
    start_time = time.time()
    for filename in camera.capture_continuous('frame.jpg'):
        print(filename)
        
        if ( ( time.time() - start_time) > initial_time):
            break
        time.sleep(shutter_speed)
    file = "img"
    for num in range(1,10):
        temp =file  +str(num) + ".jpg"
        print("remove")
        os.remove(temp)
        print(temp)
    key = cv2.waitKey(1) & 0xFF
    cv2.imshoe("Frame",camera);
    if key == ord("q"):
        break

camera.stop_preview()
camera.close()

def landmarkDetection(predictor):
    predictor_path = 
    faces_folder_path = sys.argv[2]

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
