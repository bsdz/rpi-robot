#!/usr/bin/python

import sys

from time import sleep
from Queue import Queue
from threading import Thread

from motor import MotorPair
from servo import ServoPair
from ultrasonic import Ultrasonic

from logger import Logger
log = Logger("Main").get_log()


class AutoPilot(object):
    log = Logger("Main").get_log()
    
    def __init__(self):
        self.log.info('initialize autopilot..')
        self.motor_pair = MotorPair()
        self.servo = ServoPair()
        self.ultrasonic = Ultrasonic()
            
    def run(self):
        self.log.debug('running autopilot..')

        while True:
            print self.scan_distance_periphery()
            sleep(1)

        """
            self.motor_pair.accelerate(10)
            self.motor_pair.accelerate(-10) 
            self.motor_pair.bear_left(-10)
            self.motor_pair.bear_right(-10)
            self.motor_pair.set_velocity(0)
        """
    
    def scan_distance_periphery(self):
        self.log.debug('scanning distance periphery..')

        res = {}
        self.servo.center()
        for i in (range(0,60)):
            sleep(0.01)
            self.servo.pan_left()
            res[self.servo.horizontal_servo.current_step] = self.ultrasonic.measure()

        return res

        #s.center()
        #for i in (range(0,80)):
        #    time.sleep(sleep_seconds)
        #    s.pan_right()



if __name__ == "__main__":

    ap = AutoPilot()
    ap.run()
