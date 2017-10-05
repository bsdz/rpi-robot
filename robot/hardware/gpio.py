'''
Created on 1 Oct 2017

@author: blair
'''
from unittest.mock import Mock

from robot.utility.process import execute_command
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
    
try:
    import RPi.GPIO as gpio
except:
    gpio = GpioMock()
    
try:
    from pigpio import pi, INPUT, EITHER_EDGE
except:
    pi = PIGpioMock
    INPUT = 0
    EITHER_EDGE = 1
    
def system_register():
    if os.getuid() != 0:
        log.error("Must be run as root")
        return False
        
    log.info("starting pigpiod..")
    execute_command(["pigpiod"])

    return True
    
