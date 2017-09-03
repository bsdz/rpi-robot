'''
Created on 2 Sep 2017

@author: pi
'''
import os
import argparse
import subprocess
from multiprocessing import Process
from time import sleep

from robot.utility.logger import Logger
log = Logger("Control").get_log()

from robot.webserver import start_web_application

V4L2CTL_PATH="/usr/bin/v4l2-ctl"
#WEBSERVER_PATH=./webserver.py
#FACEDETECT_PATH=./facedetect.py
#NODEJS_PATH=/usr/bin/nodejs

class CommandResults(object):
    def __init__(self, out, err, retcode):
        self.out = out
        self.err = err
        self.retcode = retcode

def execute_command(command_args):
    sp = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = sp.communicate()
    if out:
        log.info("standard output of subprocess:\n%s" % out)

    if err:
        log.info("standard error of subprocess:\n%s" % err)

    return CommandResults(out, err, sp.returncode)

def register_modules():
    log.info("registering onboard camera (/dev/video0)..")
    execute_command(["modprobe", "bcm2835-v4l2"])
    execute_command([V4L2CTL_PATH, "--set-ctrl", "video_bitrate=100000"])
    execute_command([V4L2CTL_PATH, "--set-fmt-video=width=320,height=240,pixelformat=5"])
    
    log.info("registering loopback video (/dev/video2)..")
    execute_command(["modprobe", "videodev"])
    execute_command(["modprobe", "v4l2loopback", "video_nr=2"])
  
    log.info("starting pigpiod..")
    #pigpiod >/dev/null
    execute_command(["pigpiod"])
    
def unregister_modules():
    log.info("unregistering onboard camera (/dev/video0)..")
    execute_command(["modprobe", "-r", "bcm2835-v4l2"])
    
    log.info("unregistering loopback video (/dev/video2)..")
    execute_command(["modprobe", "-r", "v4l2loopback"])
    


def start_robot():
    p = Process(target=start_web_application)
    p.start()
    #p.join()
    while True:
        sleep(0.5)

    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", action="store_true", help="")
    parser.add_argument("--restart", action="store_true", help="")
    parser.add_argument("--reload", action="store_true", help="")
    parser.add_argument("--stop", action="store_true", help="")
    parser.add_argument("--status", action="store_true", help="")
    parser.add_argument("--register", action="store_true", help="")
    parser.add_argument("--unregister", action="store_true", help="")
    args = parser.parse_args()
    
    if os.getuid() != 0:
        print("Must be run as root")
        exit(1)
    
    if args.register:
        register_modules()
    elif args.unregister:
        unregister_modules()

if __name__ == "__main__":
    main()