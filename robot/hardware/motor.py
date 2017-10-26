import sys
import asyncio

import robot.settings as settings
from robot.hardware.gpio import pigpio_instance, INPUT, EITHER_EDGE, tickDiff
from robot.utility.logger import Logger

log = Logger("Motor").get_log()

PI = 3.1415926

class Motor(object): # 7,11,13,15
    

    def __init__(self, name, pin_enable1, pin_enable2, pin_input1, pin_input2, pin_speedsensor):
        self.name = name
        self.pigpio = pigpio_instance
        
        self.pin_enable1 = pin_enable1
        self.pin_enable2 = pin_enable2
        self.pin_input1 = pin_input1
        self.pin_input2 = pin_input2
        self.pin_speedsensor = pin_speedsensor
        
        self.sensor_speed = 0 # m/s
        self.sensor_last_tick = None
        self.sensor_tick_interval_microseconds = None
        def _cbf(gpio, level, tick):
            if self.sensor_last_tick is not None:
                self.sensor_tick_interval_microseconds = tickDiff(self.sensor_last_tick, tick)
                self.sensor_speed = 1000 * PI * settings.wheel_diameter_millimetres / self.sensor_tick_interval_microseconds / settings.wheel_sensor_notches
            self.sensor_last_tick = tick
        
        self.pigpio.set_mode(self.pin_speedsensor, INPUT)
        self.pigpio.callback(self.pin_speedsensor, EITHER_EDGE, _cbf)
        
        pwm_frequency = 40 #500
        self.pigpio.set_PWM_frequency(self.pin_enable1, pwm_frequency)
        self.pigpio.set_PWM_frequency(self.pin_enable2, pwm_frequency)    
    
        self._power = 0
        self._enable = 0
        self._velocity = 0
             

    @property
    def enable(self):
        return self._enable
    
    @enable.setter
    def enable(self, value):
        self.pigpio.write(self.pin_enable1, value)
        self.pigpio.write(self.pin_enable2, value)
        self._enable = value
    
    @property
    def power(self):
        return self._power
    
    @power.setter
    def power(self, value):
        """power int: 0-255"""
        if value > 255: value = 255
        if value < 0: value = 0
        self.pigpio.set_PWM_dutycycle(self.pin_enable1, value)
        self.pigpio.set_PWM_dutycycle(self.pin_enable2, value)
        self._power = value
            
    def control(self, in1, in2, required_speed):
        """required_speed in m/s
        """
        self.pigpio.write(self.pin_input1, in1)
        self.pigpio.write(self.pin_input2, in2)
        
        log.info(f"Requested speed: {required_speed}")
        if required_speed == 0:
            self.enable = 0
            self.power = 0
        else:
            self.enable = 1
            threshold = 0.5
            n = 20
            # make n attempts to reach required speed 
            for i in range(n+1):
                log.info(f"Sensor speed: {self.sensor_speed}")
                if abs(required_speed - self.sensor_speed) < threshold:
                    break
                if required_speed > self.sensor_speed:
                    self.power -= 5
                elif required_speed < self.sensor_speed:
                    self.power += 5
                
                
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        if value is None: # coast on brake
            self.control(0, 0, 0)
        elif value > 0:
            self.control(0, 1, abs(value))
        elif value < 0:
            self.control(1, 0, abs(value))
        else: # hard brake
            self.control(1, 1, 0)
        
    def accelerate(self, delta = 1):
        self.velocity += delta
        
class MotorPair(object):
    def __init__(self):
        self.m1 = Motor("m1", 
            settings.gpio_wheel_motor_left_enable_1,
            settings.gpio_wheel_motor_left_enable_2,
            settings.gpio_wheel_motor_left_input_1,
            settings.gpio_wheel_motor_left_input_2,
            settings.gpio_wheel_sensor_left)
        
        self.m2 = Motor("m2", 
            settings.gpio_wheel_motor_right_enable_1,
            settings.gpio_wheel_motor_right_enable_2,
            settings.gpio_wheel_motor_right_input_1,
            settings.gpio_wheel_motor_right_input_2,
            settings.gpio_wheel_sensor_right)
              
    def set_velocity(self, velocity):
        self.m1.velocity = velocity
        self.m2.velocity = velocity
        
    def accelerate(self, delta):
        self.m1.accelerate(delta)
        self.m2.accelerate(delta)
        
    def bear_left(self, delta=-1):
        self.m1.accelerate(-delta)
        self.m2.accelerate(delta)
        
    def bear_right(self, delta=-1):
        self.m1.accelerate(delta)
        self.m2.accelerate(-delta)        
        
    def rotate_left(self, rotate_speed = .2):
        self.m1.velocity = rotate_speed
        self.m2.velocity = 0
        
    def rotate_right(self, rotate_speed = .2):
        self.m1.velocity = 0
        self.m2.velocity = rotate_speed

async def motor_test_routines(loop):
    
    async def input(s):
        print(s)
        await loop.run_in_executor(None, sys.stdin.readline)
    
    mp = MotorPair()
    mp.set_velocity(0)
    await input("Press Enter to continue...")

    log.info("forward")
    mp.set_velocity(.5)
    await input("Press Enter to continue...")
 
    log.info("backward")
    mp.set_velocity(-.5)
    await input("Press Enter to continue...")
 
    log.info("rotate left")
    mp.rotate_left()
    await input("Press Enter to continue...")
 
    log.info("rotate right")
    mp.rotate_right()
    await input("Press Enter to continue...")
     
    log.info("bear left")
    mp.set_velocity(.5)
    await input("Press Enter to continue...")
    mp.bear_left(.5)
    await input("Press Enter to continue...")
  
    log.info("bear left")
    mp.set_velocity(.5)
    await input("Press Enter to continue...")
    mp.bear_right(.5)
    await input("Press Enter to continue...")       
     
    log.info("accelerate test")
    mp.set_velocity(-.5)
    for i in range(0, 10):
        mp.accelerate(.1)
        await input("Press Enter to continue...")

    mp.set_velocity(0)

def main():
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(motor_test_routines(loop))


if __name__ == "__main__":
    main()
