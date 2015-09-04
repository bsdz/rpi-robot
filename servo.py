import time
import pigpio

from logger import Logger
log = Logger("Main").get_log()

class Servo(object):
    log = Logger("Servo").get_log()

    def __init__(self, name, gpio):
        self.name = name
        self.gpio = gpio
        self.min_step = 1000
        self.max_step = 2000
        self.step_size = 10 # us
        self.current = None
        self.pigpio = pigpio.pi()

    def position(self, position = None, steps_per_second = 200):
        if position:
            self.log.debug("servo %s: setting position %s" % (self.name, position))
            if not self.current:
                self.control(position)
            elif position != self.current:
                for p in range(self.current, position + 1, cmp(position, self.current)):
                    self.control(p)
                    time.sleep(1 / steps_per_second)
        return self.current

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
    log = Logger("ServoPair").get_log()

    def __init__(self):
        self.horizontal = Servo("Horizontal", 7)
        self.vertical = Servo("Vertical", 8)
        self.center()

    def set_position_coordinates(self, horiz, vert):
        self.horizontal.position(horiz)
        self.vertical.position(vert)

    def center(self):
        self.horizontal.position(1500)
        self.vertical.position(1500)

    def pan_left(self):
        self.horizontal.control(1, "-")    

    def pan_right(self):
        self.horizontal.control(1, "+")    

    def tilt_down(self):
        self.vertical.control(1, "-")    

    def tilt_up(self):
        self.vertical.control(1, "+")    
        
def main():

    s = ServoPair()
    sleep_seconds = 0.1

    log.info("test coordinates..")
    coors = [
        [1000, 1000], [1000, 2000], [2000,2000], [2000,1000], [1500,1500]
    ]
    for h,v in coors:
        s.set_position_coordinates(h, v)
        time.sleep(0.5)

    log.info("test tilt up..")
    s.center()
    for i in (range(0,80)):
        time.sleep(sleep_seconds)
        s.tilt_up()

    log.info("test tilt down..")
    s.center()
    for i in (range(0,20)):
        time.sleep(sleep_seconds)
        s.tilt_down()
    
    log.info("test pan left..")
    s.center()
    for i in (range(0,80)):
        time.sleep(sleep_seconds)
        s.pan_left()
    
    log.info("test pan right..")
    s.center()
    for i in (range(0,80)):
        time.sleep(sleep_seconds)
        s.pan_right()
    
    s.center()
    time.sleep(1)

if __name__ == "__main__":
    #import ptvsd
    #ptvsd.enable_attach(secret = 'rfvgy7', address = ('0.0.0.0', 8080))
    #ptvsd.wait_for_attach()
    main()
