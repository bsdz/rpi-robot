'''system gpio remote hardware proxy

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import os
import logging
from unittest.mock import Mock

import robot.settings as settings
from robot.utility.process import execute_command

log = logging.getLogger('pigpio').addHandler(logging.NullHandler())

class PIGpioMock(Mock):
    @staticmethod
    def get_servo_pulsewidth(pin):   
        log.info("get_servo_pulsewidth(pin %s)" % (pin))
        return 0

try:
    from pigpio import pi, INPUT, OUTPUT, EITHER_EDGE, FALLING_EDGE, RISING_EDGE, PUD_UP, PUD_DOWN, PUD_OFF, tickDiff
    # todo: if we're running on the device, use "None"
    pigpio_instance = pi(settings.robot_ip_address)
except:
    pi = PIGpioMock
    INPUT = 0
    OUTPUT = 1

    EITHER_EDGE = 2
    FALLING_EDGE = 1
    RISING_EDGE = 0

    PUD_UP = 20
    PUD_DOWN = 21
    PUD_OFF = 22
    
    tickDiff = lambda t1, t2: t2-t1
    
    pigpio_instance = pi()
    
def system_register():
    if os.getuid() != 0:  # @UndefinedVariable
        log.error("Must be run as root")
        return False
        
    log.info("starting pigpiod..")
    execute_command(["pigpiod"])

    return True
    
