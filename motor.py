import RPi.GPIO as gpio
import time

from logger import Logger
log = Logger("Main").get_log()

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

class Motor(object): # 7,11,13,15
    def __init__(self, name, pin_enable1, pin_enable2, pin_input1, pin_input2):
        self.name = name
        self.pin_enable1 = pin_enable1
        self.pin_enable2 = pin_enable2
        self.pin_input1 = pin_input1
        self.pin_input2 = pin_input2
        gpio.setup(self.pin_enable1, gpio.OUT)
        gpio.setup(self.pin_enable2, gpio.OUT)
        gpio.setup(self.pin_input1, gpio.OUT)
        gpio.setup(self.pin_input2, gpio.OUT)
        self.pwm_frequency = 40
        self.minimum_speed = 15
        self.maximum_speed = 100
        self.speed = 0
        self.direction = 0 # 1 ~ forward, 0 ~ stationary, -1 ~ backward       
        
    def __del__(self):      
        gpio.cleanup(self.pin_enable1)
        gpio.cleanup(self.pin_enable2)
        gpio.cleanup(self.pin_input1)
        gpio.cleanup(self.pin_input2)

    def enable(self, enable):
        gpio.output(self.pin_enable1, enable)
        gpio.output(self.pin_enable2, enable)
        if enable:
            self.gpio_enable1 = gpio.PWM(self.pin_enable1, self.pwm_frequency)
            self.gpio_enable2 = gpio.PWM(self.pin_enable2, self.pwm_frequency)
            self.gpio_enable1.start(self.speed)
            self.gpio_enable2.start(self.speed)
        else:
            self.gpio_enable1.stop()
            self.gpio_enable2.stop()          
    
    def control(self, in1, in2, speed = 90):
        if speed > 100: speed = self.maximum_speed
        if speed < 0: speed = 0
        self.speed = speed
        log.debug("motor %s set speed: %s; direction: %s" % (self.name, self.speed, self.direction))
        # override actual motor speed to avoid ineffective pwm duty cycle
        actual_motor_speed = self.minimum_speed if speed != 0 and speed < self.minimum_speed else speed		
        gpio.output(self.pin_input1, in1)
        gpio.output(self.pin_input2, in2)
        self.gpio_enable1.start(actual_motor_speed)
        self.gpio_enable2.start(actual_motor_speed)                                  
       
    def set_velocity(self, velocity=0, coast_on_brake=False):
        self.direction = cmp(velocity, 0)
        self.speed = abs(velocity)
        if self.direction == 1:
            self.control(False, True, self.speed)
        elif self.direction == -1:
            self.control(True, False, self.speed)
        else:
            if coast_on_brake:
                self.control(False, False, 0)
            else:
                self.control(True, True, 0)
        
    def accelerate(self, delta = 1):
        velocity = (self.speed * self.direction) + delta
        self.set_velocity(velocity) 

        
class MotorPair(object):

    def __init__(self):
        self.m1 = Motor("m1", 7,11,13,15)
        self.m2 = Motor("m2", 12,16,18,22)
        self.m1.enable(True)
        self.m2.enable(True)
        
    def __del__(self):
        self.m1.enable(False)
        self.m2.enable(False)  
              
    def set_velocity(self, velocity):
        self.m1.set_velocity(velocity)
        self.m2.set_velocity(velocity)
        
    def accelerate(self, delta):
        self.m1.accelerate(delta)
        self.m2.accelerate(delta)
        
    def bear_left(self, delta=-1, rotate_speed=50):
        if self.m2.speed == 0:
            self.m1.set_velocity(rotate_speed)
            self.m2.set_velocity(0)
        else:  
            self.m2.accelerate(delta)
        
    def bear_right(self, delta=-1, rotate_speed=50):
        if self.m2.speed == 0:
            self.m1.set_velocity(0)
            self.m2.set_velocity(rotate_speed)
        else:  
            self.m1.accelerate(delta)          
        
    def rotate_left(self, rotate_speed = 50):
        self.m1.set_velocity(rotate_speed)
        self.m2.set_velocity(0)
        
    def rotate_right(self, rotate_speed = 50):
        self.m1.set_velocity(0)
        self.m2.set_velocity(rotate_speed)

def main():
    mp = MotorPair()
    raw_input("Press Enter to continue...")
    
    print "forward"
    mp.set_velocity(40)
    raw_input("Press Enter to continue...")

    print "backward"
    mp.set_velocity(-40)
    raw_input("Press Enter to continue...")

    print "rotate left"
    mp.rotate_left()
    raw_input("Press Enter to continue...")

    print "rotate right"
    mp.rotate_right()
    raw_input("Press Enter to continue...")
    
    print "bear left"
    mp.set_velocity(50)
    raw_input("Press Enter to continue...")
    mp.bear_left(10)
    raw_input("Press Enter to continue...")
 
    print "bear left"
    mp.set_velocity(50)
    raw_input("Press Enter to continue...")
    mp.bear_right(10)
    raw_input("Press Enter to continue...")       
    
    print "accelerate test"
    mp.set_velocity(-50)
    for i in xrange(0,9):
        mp.accelerate(10)
        raw_input("Press Enter to continue...")


if __name__ == "__main__":
    #import ptvsd
    #ptvsd.enable_attach(secret = 'rfvgy7', address = ('0.0.0.0', 8080))
    #ptvsd.wait_for_attach()
    main()
