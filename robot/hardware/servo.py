'''camera servos

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''

import time
import logging

import robot.settings as settings
from robot.proxy.pigpio import pigpio_instance

class Servo(object):
    def __init__(self, name, gpio, minimum = 1000, maximum = 2000, center = 1500):
        self.name = name
        
        self.log = logging.getLogger(f'servo {name}')

        self.gpio = gpio
        self.min_step = minimum
        self.max_step = maximum
        self.center_step = center
        self.step_size = 10 # us
        self.current = None
        self.pigpio = pigpio_instance

    def position(self, position = None, steps_per_second = 200):
        if position:
            self.log.debug("servo %s: setting position %s" % (self.name, position))
            if not self.current:
                self.control(position)
            elif position != self.current:
                cmp = (position > self.current) - (position < self.current)
                for p in range(self.current, position + 1, cmp):
                    self.control(p)
                    time.sleep(1 / steps_per_second)
        return self.current

    def center(self):
        return self.control(self.center_step)

    def control(self, step, modifier=None):
        if not modifier and (step < self.min_step or step > self.max_step):
            return

        if modifier == "+":
            self.current = self.pigpio.get_servo_pulsewidth(self.gpio) + step
        elif modifier == "-":
            self.current = self.pigpio.get_servo_pulsewidth(self.gpio) - step
        else:
            self.current = step
        
        self.log.debug("servo %s (%s): set to '%s'" % (self.name, self.gpio, self.current))
        self.pigpio.set_servo_pulsewidth(self.gpio, self.current) # todo: check return value

class ServoPair(object):
 
    def __init__(self):
        
        self.horizontal = Servo("Horizontal", settings.gpio_camera_servo_horizontal, 
                                settings.camera_servo_horizontal_minimum, 
                                settings.camera_servo_horizontal_maximum,
                                settings.camera_servo_horizontal_center)
        self.vertical = Servo("Vertical", settings.gpio_camera_servo_vertical, 
                                settings.camera_servo_vertical_minimum, 
                                settings.camera_servo_vertical_maximum,
                                settings.camera_servo_vertical_center)
        self.center()

    def set_position_coordinates(self, horiz, vert):
        self.horizontal.position(horiz)
        self.vertical.position(vert)

    def center(self):
        self.horizontal.center()
        self.vertical.center()

    def pan_left(self):
        self.horizontal.control(1, "-")    

    def pan_right(self):
        self.horizontal.control(1, "+")    

    def tilt_down(self):
        self.vertical.control(1, "-")    

    def tilt_up(self):
        self.vertical.control(1, "+")    
        
def main():
    from robot.utility.logging import console_log_handler
    logger = logging.getLogger('')
    logger.addHandler(console_log_handler)
    logger.setLevel(logging.DEBUG)

    s = ServoPair()
    sleep_seconds = 0.1

    logger.info("test coordinates..")
    coors = [
        [550, 830], [550, 830], [2050,2300], [2050,2300], [1250,900]
    ]
    for h,v in coors:
        s.set_position_coordinates(h, v)
        time.sleep(0.5)

    logger.info("test tilt up..")
    s.center()
    for i in (range(0,80)):
        time.sleep(sleep_seconds)
        s.tilt_up()

    logger.info("test tilt down..")
    s.center()
    for i in (range(0,20)):
        time.sleep(sleep_seconds)
        s.tilt_down()
    
    logger.info("test pan left..")
    s.center()
    for i in (range(0,80)):
        time.sleep(sleep_seconds)
        s.pan_left()
    
    logger.info("test pan right..")
    s.center()
    for i in (range(0,80)):
        time.sleep(sleep_seconds)
        s.pan_right()
    
    s.center()
    time.sleep(1)

if __name__ == "__main__":
    
    main()
