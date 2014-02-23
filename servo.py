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
        self.current_step = None
        self.device = open('/dev/servoblaster', 'w')

    def control(self, step, modifier=""):
        instruction = "%s=%s%s" % (self.id, modifier, step)
        #log.debug("Send: '%s'" % instruction)
        self.device.write(instruction + "\n")
        self.device.flush()
        if modifier == "-":
            self.current_step -= step
        elif modifier == "+":
            self.current_step += step
        else:   
            self.current_step = step

class ServoPair(object):
    def __init__(self):
        self.horizontal_servo = Servo("Horizontal", 0)
        self.vertical_servo = Servo("Vertical", 1)

    def set_step_coordinate(self, horiz, vert):
        self.horizontal_servo.control(horiz)
        self.vertical_servo.control(vert)

    def pan_left(self):
        self.horizontal_servo.control(1, "-")    

    def pan_right(self):
        self.horizontal_servo.control(1, "+")    

    def tilt_down(self):
        self.vertical_servo.control(1, "-")    

    def tilt_up(self):
        self.vertical_servo.control(1, "+")    

    def center(self):
        self.set_step_coordinate(125, 95)
        
def main():
    coors = [
        [90, 90], [90, 210], [210,210], [210,90], [125,95]
    ]
    s = ServoPair()
    for h,v in coors:
        s.set_step_coordinate(h, v)
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
