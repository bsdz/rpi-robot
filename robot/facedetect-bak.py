#!/usr/bin/python
 
from sys import path
path.append("./opencv-patched/lib/python2.7/dist-packages/")

import cv2
import time
import numpy as np

from v4l2loopback import V4L2Loopback

def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()
    
def draw_string(image, (x, y), s):
    cv2.putText(image, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv2.LINE_AA)
    cv2.putText(image, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)    

def create_image(width, height, depth, channels):
    return np.zeros((height,width,3), np.uint8)
    
def detect(image, cascade):
    rectangles = cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rectangles) == 0:
        return []
    rectangles[:,2:] += rectangles[:,:2]
    return rectangles

def draw_rectangles(image, rectangles, color):
    for x1, y1, x2, y2 in rectangles:
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)    
 
def main():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    capture.set(cv2.CAP_PROP_FPS, 1)
    #
    #capture.set(cv2.CAP_PROP_CONTRAST, 0)
    #capture.set(cv2.CAP_PROP_SATURATION, 0)
    #capture.set(cv2.CAP_PROP_HUE, )
    #capture.set(cv2.CAP_PROP_GAIN, )
    #time.sleep(2) 
    #capture.set(cv2.CAP_PROP_EXPOSURE, -8)  
    capture.set(cv2.CAP_PROP_BRIGHTNESS, 0.6)
     
    
    loopback = V4L2Loopback(320, 240, 3)
    
    detect_eyes = False

    cascade_dir = r"./opencv-patched/share/OpenCV/haarcascades/" 
    #face_cascade = cv2.CascadeClassifier("%s/haarcascade_frontalface_default.xml" % (cascade_dir))
    #face_cascade = cv2.CascadeClassifier("%s/haarcascade_frontalface_alt2.xml" % (cascade_dir))    
    #face_cascade = cv2.CascadeClassifier("%s/haarcascade_frontalface_alt_tree.xml" % (cascade_dir))
    face_cascade = cv2.CascadeClassifier("%s/haarcascade_frontalface_alt.xml" % (cascade_dir))
    eye_cascade = cv2.CascadeClassifier("%s/haarcascade_eye.xml" % (cascade_dir))
    
    while True:
        t = clock()
        success, captured_image = capture.read()
        if success:
            grayscale_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2GRAY)
            grayscale_image = cv2.equalizeHist(grayscale_image)

            rectangles = detect(grayscale_image, face_cascade)
            output_image = captured_image.copy()
            draw_rectangles(output_image, rectangles, (0, 255, 0))
            if detect_eyes:
                for x1, y1, x2, y2 in rectangles:
                    grayscale_subimage = grayscale_image[y1:y2, x1:x2]
                    output_subimage = output_image[y1:y2, x1:x2]
                    subrectangles = detect(grayscale_subimage.copy(), eye_cascade)            
                    draw_rectangles(output_subimage, subrectangles, (255, 0, 0))

            dt = clock() - t
            draw_string(output_image, (20, 20), 'time: %.1f ms' % (dt*1000))
            #cv2.imshow('facedetect', captured_image)
            loopback.write(bytearray(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)))

            if 0xFF & cv2.waitKey(5) == 27:
                break
                
        time.sleep(1)
            
    cv2.destroyAllWindows()    

if __name__ == "__main__":
    main()
