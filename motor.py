import RPi.GPIO as gpio
import time

from logger import Logger
log = Logger("Main").get_log()

class Motor(object):
    def __init__(self):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BOARD)
        gpio.setup(7, gpio.OUT)  # m0 enable 1
        gpio.setup(11, gpio.OUT) # m0 enable 2
        gpio.setup(13, gpio.OUT) # m0 input 1
        gpio.setup(15, gpio.OUT) # m0 input 2
        gpio.setup(12, gpio.OUT) # m1 enable 1
        gpio.setup(16, gpio.OUT) # m1 enable 2
        gpio.setup(18, gpio.OUT) # m1 input 1
        gpio.setup(22, gpio.OUT) # m1 input 2
        self.pwm_frequency = 40
        self.minimum_speed = 15
        self.maximum_speed = 100
        self.speed = { 0: 0, 1: 0 }
        self.direction = { 0: 0, 1: 0 } # 1 ~ forward, 0 ~ stationary, -1 ~ backward
        
        
    def __del__(self):      
        gpio.cleanup()

    def enable(self, m, enable):
        if m == 0:
            gpio.output(7, enable)
            gpio.output(11, enable)
            if enable:
                self.p7 = gpio.PWM(7, self.pwm_frequency)
                self.p11 = gpio.PWM(11, self.pwm_frequency)
                self.p7.start(self.speed[m])
                self.p11.start(self.speed[m])
            else:
                self.p7.stop()
                self.p11.stop()          
        if m == 1:
            gpio.output(12, enable)
            gpio.output(16, enable)
            if enable:
                self.p12 = gpio.PWM(12, self.pwm_frequency)
                self.p16 = gpio.PWM(16, self.pwm_frequency)
                self.p12.start(self.speed[m])
                self.p16.start(self.speed[m])
            else:
                self.p12.stop()
                self.p16.stop()
    
    def control(self, m, in1, in2, speed = 90):
        if speed > 100: speed = self.maximum_speed
        if speed < 0: speed = 0
        self.speed[m] = speed
        log.debug("motor %s set speed: %s; direction: %s" % (m, self.speed[m], self.direction[m]))
        # override actual motor speed to avoid ineffective pwm duty cycle
        actual_motor_speed = self.minimum_speed if speed != 0 and speed < self.minimum_speed else speed
        if m == 0:			
            gpio.output(13, in1)
            gpio.output(15, in2)
            self.p7.start(actual_motor_speed)
            self.p11.start(actual_motor_speed)                  
        if m == 1:			
            gpio.output(18, in1)
            gpio.output(22, in2)
            self.p12.start(actual_motor_speed)
            self.p16.start(actual_motor_speed)                 

    def off_coast(self, m):
        self.direction[m] = 0
        self.control(m, False, False, 0)

    def off_brake(self, m):
        self.direction[m] = 0
        self.control(m, True, True, 0)

    def backward(self, m, speed = 90):
        self.direction[m] = -1
        self.control(m, True, False, speed)

    def forward(self, m, speed = 90):
        self.direction[m] = 1
        self.control(m, False, True, speed)
        
    def set_velocity(self, m, velocity):
        direction = cmp(velocity, 0)
        speed = abs(velocity)
        if direction == 1:
            self.forward(m, speed)
        elif direction == -1:
            self.backward(m, speed)
        else:
            self.off_brake(m)
        
    def accelerate(self, m, delta = 1):
        velocity = (self.speed[m] * self.direction[m]) + delta
        self.set_velocity(m, velocity) 

def main():
    m = Motor()
    print "enable motors"
    m.enable(0, True)
    m.enable(1, True)
    raw_input("Press Enter to continue...")
    
    print "0 = forward, 1 = forward"
    m.forward(0, 40)
    m.forward(1, 40)
    raw_input("Press Enter to continue...")

    print "0 = backward, 1 = backward"
    m.backward(0)
    m.backward(1)
    raw_input("Press Enter to continue...")

    print "0 = backward, 1 = stop"
    m.backward(0)
    m.off_brake(1)
    raw_input("Press Enter to continue...")

    print "0 = stop, 1 = backward"
    m.off_brake(0)
    m.backward(1)
    raw_input("Press Enter to continue...")
    
    print "accelerate test"
    m.set_velocity(0, -50)
    m.set_velocity(1, -50)
    for i in xrange(0,9):
        m.accelerate(0, 10)
        m.accelerate(1, 10)
        raw_input("Press Enter to continue...")

    print "disable motors"
    m.enable(0, False)
    m.enable(1, False)

if __name__ == "__main__":
    #import ptvsd
    #ptvsd.enable_attach(secret = 'rfvgy7', address = ('0.0.0.0', 8080))
    #ptvsd.wait_for_attach()
    main()
