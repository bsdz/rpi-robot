import time
import threading

from robot.hardware.gpio import pigpio_instance, INPUT, OUTPUT, PUD_DOWN, FALLING_EDGE, tickDiff
from robot.utility.logger import Logger
log = Logger("Main").get_log()

class Ultrasonic(object):
    log = Logger("Ultrasonic").get_log()

    def __init__(self, name = "Main", gpio_trigger = 9, gpio_echo = 10):
        self.name = name
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo
        
        self.pigpio = pigpio_instance
        self.pigpio.set_mode(gpio_trigger, OUTPUT)
        self.pigpio.set_mode(gpio_echo, INPUT)
        self.pigpio.set_pull_up_down(gpio_echo, PUD_DOWN)
        
        self.event = threading.Event()
        
    def measure(self):
        self.distance = None
        self.event.clear()
        
        self.pigpio.write(self.gpio_trigger, 0) # set to low
                
        def cbf(gpio, level, tick):
            # distance pulse travelled in that time is time
            # multiplied by the speed of sound (m/s)
            ping_micros = tickDiff(self.start_tick, tick)
            self.distance = (ping_micros * 340.29) / 2 / 1000
            self.event.set()
        
        self.pigpio.callback(self.gpio_echo, FALLING_EDGE, cbf)
        
        # Send 10us pulse to trigger        
        self.start_tick = self.pigpio.get_current_tick()
        self.pigpio.gpio_trigger(self.gpio_trigger, 10, 1)
        self.event.wait()
                
        return self.distance
     
def main():
    us = Ultrasonic("Main", 9, 10)
    input("Press Enter to continue...")
    
    print("measure")
    while True:
        print(us.measure())
        time.sleep(0.2)
    input("Press Enter to continue...")


if __name__ == "__main__":
    main()
