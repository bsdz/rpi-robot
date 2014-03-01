import time

from logger import Logger
log = Logger("Servo").get_log()

class Servo(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.min_step = 50
        self.max_step = 250
        self.step_size = 10 # us
        self.current = None
        self.device = open('/dev/servoblaster', 'w')

    def position(self, position = None, steps_per_second = 200):
        if position:
            log.debug("servo %s: setting position %s" % (self.name, position))
            if not self.current:
                self.control(position)
            elif position != self.current:
                for p in range(self.current, position + 1, cmp(position, self.current)):
                    self.control(p)
                    time.sleep(1 / steps_per_second)
        return self.current

    def control(self, step, modifier=""):
        if modifier == "" and (step < self.min_step or step > self.max_step):
            return
        instruction = "%s=%s%s" % (self.id, modifier, step)
        self.device.write(instruction + "\n")
        self.device.flush()
        #log.debug("servo %s: send instruction '%s'" % (self.name, instruction))
        if modifier == "-":
            self.current -= step
        elif modifier == "+":
            self.current += step
        else:   
            self.current = step

class ServoPair(object):
    def __init__(self):
        self.horizontal = Servo("Horizontal", 0)
        self.vertical = Servo("Vertical", 1)

    def set_position_coordinates(self, horiz, vert):
        self.horizontal.position(horiz)
        self.vertical.position(vert)

    def center(self):
        self.horizontal.position(125)
        self.vertical.position(95)

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
    sleep_seconds = 0.01

    log.info("test coordinates..")
    coors = [
        [90, 90], [90, 210], [210,210], [210,90], [125,95]
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
