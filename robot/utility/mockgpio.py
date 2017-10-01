'''
Created on 1 Oct 2017

@author: blair
'''
from unittest.mock import Mock

from robot.utility.logger import Logger
log = Logger("GPIO Mock").get_log()

class GpioMock(Mock):
    @staticmethod
    def output(pin, value):
        log.info("output(pin %s, value %s)" % (pin, value))
     

class PIGpioMock(Mock):
    @staticmethod
    def get_servo_pulsewidth(pin):   
        log.info("get_servo_pulsewidth(pin %s)" % (pin))
        return 0