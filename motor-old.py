import RPi.GPIO as gpio
import time

from logger import Logger
log = Logger("Main").get_log()

class Motor(object):
    def __init__(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BOARD)
        gpio.setup(7, gpio.OUT)
        gpio.setup(11, gpio.OUT)
        gpio.setup(13, gpio.OUT)
        gpio.setup(15, gpio.OUT)
        gpio.setup(12, gpio.OUT)
        gpio.setup(16, gpio.OUT)
        gpio.setup(18, gpio.OUT)
        gpio.setup(22, gpio.OUT)

    def enable(self, m, enable):
        if m == 0:
            gpio.output(7, enable)
            gpio.output(11, enable)
        if m == 1:
            gpio.output(12, enable)
            gpio.output(16, enable)

    def control(self, m, in1, in2):
        if m == 0:
            log.debug("start motor 1")			
            gpio.output(13, in1)
            gpio.output(15, in2)
        if m == 1:
            log.debug("start motor 2")			
            gpio.output(18, in1)
            gpio.output(22, in2)

    def off_coast(self, m):
        self.control(m, False, False)

    def off_brake(self, m):
        self.control(m, True, True)

    def backward(self, m):
        self.control(m, True, False)

    def forward(self, m):
        self.control(m, False, True)

def main():
    m = Motor()
    m.enable(0, True)
    m.enable(1, True)

    m.forward(0)
    m.forward(1)
    raw_input("Press Enter to continue...")

    m.backward(0)
    m.backward(1)
    raw_input("Press Enter to continue...")

    m.backward(0)
    m.off_brake(1)
    raw_input("Press Enter to continue...")

    m.off_brake(0)
    m.backward(1)
    raw_input("Press Enter to continue...")

    m.enable(0, False)
    m.enable(1, False)

if __name__ == "__main__":
    #import ptvsd
    #ptvsd.enable_attach(secret = 'rfvgy7', address = ('0.0.0.0', 8080))
    #ptvsd.wait_for_attach()
    main()
