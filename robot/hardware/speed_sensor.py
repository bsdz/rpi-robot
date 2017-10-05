import time

from robot.hardware.gpio import pigpio_instance, INPUT, EITHER_EDGE
from robot.utility.logger import Logger
log = Logger("Main").get_log()

def cbf(gpio, level, tick):
    print(gpio, level, tick)

class SpeedSensor(object):
    log = Logger("SpeedSensor").get_log()

    def __init__(self, name, gpio1, gpio2):
        self.name = name
        self.gpio1 = gpio1
        self.gpio2 = gpio2
        self.pigpio = pigpio_instance

        self.pigpio.set_mode(gpio1, INPUT)
        self.pigpio.set_mode(gpio2, INPUT)

        self.pigpio.callback(gpio1, EITHER_EDGE, cbf)
        self.pigpio.callback(gpio2, EITHER_EDGE, cbf)
        
def main():

    s = SpeedSensor("motor speed sensors", 19, 26)

    import time
    while True:
        time.sleep(.1)

if __name__ == "__main__":
    main()
