'''ultrasonic sensor 

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import time
import threading

import robot.settings as settings
from robot.proxy.pigpio import pigpio_instance, INPUT, OUTPUT, PUD_DOWN, FALLING_EDGE, tickDiff
from robot.utility.logger import Logger
log = Logger("Main").get_log()

class Ultrasonic(object):
    log = Logger("Ultrasonic").get_log()

    def __init__(self, name = "Main", gpio_trigger = settings.gpio_ultrasonic_trigger, gpio_echo = settings.gpio_ultrasonic_echo):
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
            self.distance = (ping_micros * 340.29) / 2 / 1000000
            self.event.set()
        
        self.pigpio.callback(self.gpio_echo, FALLING_EDGE, cbf)
        
        # Send 10us pulse to trigger        
        self.start_tick = self.pigpio.get_current_tick()
        self.pigpio.gpio_trigger(self.gpio_trigger, 10, 1)
        self.event.wait()
                
        return self.distance
     
def main():
    us = Ultrasonic()
    input("Press Enter to continue...")
    
    print("measure")
    while True:
        print(us.measure())
        time.sleep(0.5)
    input("Press Enter to continue...")


if __name__ == "__main__":
    main()
