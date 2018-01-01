'''camera

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import asyncio
import os
import logging

from picamera import PiCamera
from picamera.array import PiRGBArray

import robot.settings as settings
from robot.utility.process import execute_command

log = logging.getLogger('camera').addHandler(logging.NullHandler())

V4L2CTL_PATH="/usr/bin/v4l2-ctl"

class Camera(object):
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.count = 0
        self.camera = PiCamera()
        self.camera.resolution = (settings.video_width, settings.video_height)
        self.camera.framerate = 32
        self.output = PiRGBArray(self.camera, size=(settings.video_width, settings.video_height))

    def read(self):
        self.camera.capture(self.output, 'rgb')
        self.output.truncate(0)
        self.count += 1
        return True, self.output.array

    async def async_read(self):
        return await self.loop.run_in_executor(None, self.read)

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
