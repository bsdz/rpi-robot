#!/usr/bin/python

import sys

from time import sleep
from Queue import Queue
from threading import Thread

from motor import MotorPair
from servo import ServoPair
from ultrasonic import Ultrasonic

from logger import Logger
#log = Logger("Main").get_log()


class AutoPilot(object):
    log = Logger("Main").get_log()
    
    def __init__(self):
        self.log.info('initialize autopilot..')
        self.motor_pair = MotorPair()
        self.servo_pair = ServoPair()
        self.ultrasonic = Ultrasonic()
            
    def run(self):
        self.log.debug('running autopilot..')

        while True:
            res = self.radial_distance_scan()
            # choose max distance
            target_dir = max(res, key=res.get)
            # rotate facing max distance
            # move forward while monitor distance until min distance reached
            sleep(1)

        """
            self.motor_pair.accelerate(10)
            self.motor_pair.accelerate(-10) 
            self.motor_pair.bear_left(-10)
            self.motor_pair.bear_right(-10)
            self.motor_pair.set_velocity(0)
        """
    
    def radial_distance_scan(self):
        self.log.debug('scanning radial distance..')

        res = {}
        center_position = self.servo_pair.horizontal.default_position()
        for i in (range(center_position - 60, center_position + 60)):
            sleep(0.01)
            self.servo_pair.horizontal.current_position(i)
            distance = self.ultrasonic.measure()
            res[i] = distance
        return res

if __name__ == "__main__":

    ap = AutoPilot()
    ap.run()
