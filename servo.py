import time

from logger import Logger
log = Logger("Servo").get_log()

class Servo(object):
    def __init__(self, name, id, default_position):
        self.name = name
        self.id = id
        self.min_step = 50
        self.max_step = 250
        self.step_size = 10 # us
        self.current = None
        self.default = default_position
        self.device = open('/dev/servoblaster', 'w')

    def default_position(self, position = None):
        if position:
            self.default = position
        return self.default

    def current_position(self, position):
        if position:
            self.control(position)
        return self.current

    def control(self, step, modifier=""):
        if not step:
            step = self.default
        instruction = "%s=%s%s" % (self.id, modifier, step)
        self.device.write(instruction + "\n")
        self.device.flush()
        #log.debug("Send: '%s'" % instruction)
        if modifier == "-":
            self.current -= step
        elif modifier == "+":
            self.current += step
        else:   
            self.current = step

class ServoPair(object):
    def __init__(self):
        self.horizontal = Servo("Horizontal", 0, 125)
        self.vertical = Servo("Vertical", 1, 95)

    def set_position_coordinates(self, horiz, vert):
        self.horizontal.control(horiz)
        self.vertical.control(vert)

    def pan_left(self):
        self.horizontal.control(1, "-")    

    def pan_right(self):
        self.horizontal.control(1, "+")    

    def tilt_down(self):
        self.vertical.control(1, "-")    

    def tilt_up(self):
        self.vertical.control(1, "+")    

    def center(self):
        # sets to default
        self.set_position_coordinates(None, None)
        
def main():
    coors = [
        [90, 90], [90, 210], [210,210], [210,90], [125,95]
    ]
    s = ServoPair()
    for h,v in coors:
        s.set_position_coordinates(h, v)
        time.sleep(0.5)

    sleep_seconds = 0.01

    s.center()
    for i in (range(0,80)):
        time.sleep(sleep_seconds)
        s.tilt_up()

    s.center()
    for i in (range(0,20)):
        time.sleep(sleep_seconds)
        s.tilt_down()

    s.center()
    for i in (range(0,80)):
        time.sleep(sleep_seconds)
        s.pan_left()

    s.center()
    for i in (range(0,80)):
        time.sleep(sleep_seconds)
        s.pan_right()

    s.center()


if __name__ == "__main__":
    #import ptvsd
    #ptvsd.enable_attach(secret = 'rfvgy7', address = ('0.0.0.0', 8080))
    #ptvsd.wait_for_attach()
    main()
