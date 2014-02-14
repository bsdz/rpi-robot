#!/usr/bin/python
 
from sys import path
path.append("./opencv-patched/lib/python2.7/dist-packages/")

import cv2
import time
import numpy as np

def main():
    capture = cv2.VideoCapture(2)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
 
    while (cv2.waitKey(15) == -1):
        status, image = capture.read()
        cv2.imshow("loopback read test", image)

if __name__ == "__main__":
    main()
