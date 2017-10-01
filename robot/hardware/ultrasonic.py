import time

try:
    import RPi.GPIO as gpio
except:
    from robot.utility.mockgpio import GpioMock
    gpio = GpioMock()
    
from robot.utility.logger import Logger
log = Logger("Main").get_log()

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

class Ultrasonic(object): # 21 trigger, 19 echo
    log = Logger("Ultrasonic").get_log()

    def __init__(self, name = "Main", pin_trigger = 21, pin_echo = 19):
        self.name = name
        self.pin_trigger = pin_trigger
        self.pin_echo = pin_echo
        gpio.setup(self.pin_trigger, gpio.OUT)
        gpio.setup(self.pin_echo, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        #time.sleep(0.5) # let settle
        
    def __del__(self):      
        gpio.cleanup(self.pin_trigger)
        gpio.cleanup(self.pin_echo)

    def measure(self):
        gpio.output(self.pin_trigger, False) # set to low

        # Send 10us pulse to trigger
        gpio.output(self.pin_trigger, True)
        time.sleep(0.00001)
        gpio.output(self.pin_trigger, False)

        start = time.time()
        while gpio.input(self.pin_echo) == 0:
            start = time.time()
        stop = time.time()
        while gpio.input(self.pin_echo) == 1:
            stop = time.time()
        
        # distance pulse travelled in that time is time
        # multiplied by the speed of sound (m/s)
        return 340 * (stop - start) / 2
        
def main():
    us = Ultrasonic("Main", 21, 19)
    input("Press Enter to continue...")
    
    print("measure")
    while True:
        print(us.measure())
        time.sleep(0.2)
    input("Press Enter to continue...")


if __name__ == "__main__":
    main()
