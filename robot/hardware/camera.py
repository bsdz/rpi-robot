'''
Created on 3 Oct 2017

@author: blair
'''
import os
import cv2

import robot.settings as settings
from robot.utility.process import execute_command
from robot.utility.logger import Logger
log = Logger("Camera").get_log()

V4L2CTL_PATH="/usr/bin/v4l2-ctl"

class Camera(object):
    def __init__(self):
        self.video_capture = cv2.VideoCapture(settings.video_capture_device)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, settings.video_width)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.video_height)

    def read(self):
        return self.video_capture.read()

def system_register():
    if os.getuid() != 0:  # @UndefinedVariable
        log.error("Must be run as root")
        return False
    
    log.info("registering onboard camera (/dev/video0)..")
    execute_command(["modprobe", "bcm2835-v4l2"])
    execute_command([V4L2CTL_PATH, "--set-ctrl", "video_bitrate=100000"])
    execute_command([V4L2CTL_PATH, "--set-fmt-video=width=320,height=240,pixelformat=5"])
    
    log.info("starting pigpiod..")
    execute_command(["pigpiod"])

    return True
    
def system_unregister():
    if os.getuid() != 0:  # @UndefinedVariable
        log.error("Must be run as root")
        return False
    
    log.info("unregistering onboard camera (/dev/video0)..")
    execute_command(["modprobe", "-r", "bcm2835-v4l2"])
    return True