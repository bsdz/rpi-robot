#!/usr/bin/python
 
from sys import path
path.append("./opencv-patched/lib/python2.7/dist-packages/")

import time
import numpy as np
import v4l2
import fcntl
import os

from logger import Logger
log = Logger("Main").get_log()

class V4L2Loopback(object):
    def __init__(self, width = 640, height = 480, channels = 2):
        self.loopback_dev = os.open('/dev/video2', os.O_RDWR)
    
        vid_cap = v4l2.v4l2_capability()
        ret_code = fcntl.ioctl(self.loopback_dev, v4l2.VIDIOC_QUERYCAP, vid_cap)
        log.debug("VIDIOC_QUERYCAP returned %s" % (ret_code))
        
        vid_format = v4l2.v4l2_format()
        vid_format.type = v4l2.V4L2_BUF_TYPE_VIDEO_OUTPUT
        vid_format.fmt.pix.width = width
        vid_format.fmt.pix.height = height
        vid_format.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_RGB24
        #vid_format.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_YUYV
        #vid_format.fmt.pix.pixelformat = v4l2.V4L2_PIX_FMT_YVU420
        vid_format.fmt.pix.sizeimage = width * height * channels
        vid_format.fmt.pix.field = v4l2.V4L2_FIELD_NONE
        vid_format.fmt.pix.bytesperline = width * channels
        #vid_format.fmt.pix.colorspace = v4l2.V4L2_COLORSPACE_JPEG
        vid_format.fmt.pix.colorspace = v4l2.V4L2_COLORSPACE_SRGB
        
        ret_code = fcntl.ioctl(self.loopback_dev, v4l2.VIDIOC_S_FMT, vid_format)
        log.debug("VIDIOC_S_FMT returned %s" % (ret_code))
        
    def __del__(self):
        os.close(self.loopback_dev) 
        
    def write(self, bytes):
        os.write(self.loopback_dev, bytes)

def create_image(width, height, depth, channels):
    return np.zeros((height,width,channels), np.uint8)
 
def main():
    loopback = V4L2Loopback(640, 480, 3)
    image = np.zeros((640,480,3), np.uint8)
    loopback.write(bytearray(image))
    raw_input("press a key to finish")

if __name__ == "__main__":
    main()
    
