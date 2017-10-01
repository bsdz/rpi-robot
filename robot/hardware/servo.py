import time

try:
    from pigpio import pi
except:
    from robot.utility.mockgpio import PIGpioMock
    pi = PIGpioMock

from robot.utility.logger import Logger
log = Logger("Main").get_log()

class Servo(object):
    log = Logger("Servo").get_log()

    def __init__(self, name, gpio, minimum = 1000, maximum = 2000, center = 1500):
        self.name = name
        self.gpio = gpio
        self.min_step = minimum
        self.max_step = maximum
        self.center_step = center
        self.step_size = 10 # us
        self.current = None
        self.pigpio = pi()

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
    log = Logger("ServoPair").get_log()

    def __init__(self):
        self.horizontal = Servo("Horizontal", 8, 550, 2050, 1250)
        self.vertical = Servo("Vertical", 7, 830, 2300, 900)
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

    s = ServoPair()
    sleep_seconds = 0.1

    log.info("test coordinates..")
    coors = [
        [550, 830], [550, 830], [2050,2300], [2050,2300], [1250,900]
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
