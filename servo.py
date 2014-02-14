import time

from logger import Logger
log = Logger("Main").get_log()

class Servo(object):
    def __init__(self):
        self.servoblaster = open('/dev/servoblaster', 'w')

    def control(self, s, value, unit="%", modifier=""):
        instruction = "%s=%s%s%s" % (s, modifier, value, unit)
        log.debug("Send: '%s'" % instruction)
        self.servoblaster.write(instruction + "\n")
        self.servoblaster.flush()

    def set_pan_percent(self, pct):
        self.control(0, pct)

    def set_tilt_percent(self, pct):
        self.control(1, pct)

    def pan_left(self):
        self.control(0, 5, "", "-")    

    def pan_right(self):
        self.control(0, 5, "", "+")    

    def tilt_down(self):
        self.control(1, 5, "", "-")    

    def tilt_up(self):
        self.control(1, 5, "", "+")    

    def center(self):
        self.control(0, 40)
        self.control(1, 20)


def main():
    sleep_seconds=0.5
    s = Servo()
    s.set_pan_percent(10)
    time.sleep(sleep_seconds)
    s.set_pan_percent(80)
    time.sleep(sleep_seconds)
    s.set_pan_percent(40)
    time.sleep(sleep_seconds)
    s.set_tilt_percent(20)
    time.sleep(sleep_seconds)
    s.set_tilt_percent(80)
    time.sleep(sleep_seconds)
    s.set_tilt_percent(20)
    for i in (range(0,10)):
        time.sleep(sleep_seconds)
        s.tilt_up()
    for i in (range(0,10)):
        time.sleep(sleep_seconds)
        s.tilt_down()
    for i in (range(0,10)):
        time.sleep(sleep_seconds)
        s.pan_left()
    for i in (range(0,10)):
        time.sleep(sleep_seconds)
        s.pan_right()
    s.center()


if __name__ == "__main__":
    #import ptvsd
    #ptvsd.enable_attach(secret = 'rfvgy7', address = ('0.0.0.0', 8080))
    #ptvsd.wait_for_attach()
    main()
