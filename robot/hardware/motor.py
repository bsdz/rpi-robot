'''wheel motors

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import sys
import os
import asyncio
import logging
from tempfile import tempdir

import numpy as np

import robot.settings as settings
from robot.utility.helpers import range_bound
from robot.proxy.pigpio import pigpio_instance, INPUT, FALLING_EDGE, tickDiff

PI = 3.1415926

class Motor(object): # 7,11,13,15
    
    def __init__(self, name, pin_enable1, pin_enable2, pin_input1, pin_input2, pin_speedsensor, loop=None):
        self.name = name
        
        self.loop = loop
        
        self.log = logging.getLogger(f'motor {name}')
        
        self.pigpio = pigpio_instance
        
        self.pin_enable1 = pin_enable1
        self.pin_enable2 = pin_enable2
        self.pin_input1 = pin_input1
        self.pin_input2 = pin_input2
        self.pin_speedsensor = pin_speedsensor
        
        self._sensor_speed = 0 # m/s
        self.sensor_last_tick = None
        self.sensor_tick_interval_microseconds = None
        def _cbf(gpio, level, tick):
            if gpio == self.pin_speedsensor and self.sensor_last_tick is not None:
                self.sensor_tick_interval_microseconds = tickDiff(self.sensor_last_tick, tick)
                self._sensor_speed = 1000 * PI * settings.wheel_diameter_millimetres / self.sensor_tick_interval_microseconds / settings.wheel_sensor_notches
            self.sensor_last_tick = tick
        
        self.frequency = 40 # 40  or 500 
    
        self._velocity = 0

        self.pigpio.set_glitch_filter(self.pin_speedsensor, 100)
        self.pigpio.set_mode(self.pin_speedsensor, INPUT)
        self.pigpio.callback(self.pin_speedsensor, FALLING_EDGE, _cbf)
        
        self._power = 0
    
    async def calibrate(self):
        self.control(0, 1, 1)
        await asyncio.sleep(3)
        out_path = os.path.join(tempdir(), "motor-calibration-%s.csv" % self.name)
        with open(out_path, "w") as fh:
            for f in range(50, 1000, 100):
                print(f'frequency: {f}')
                self.sensor_speed = 0
                for p in range(1, 256, 10):
                    self.frequency = f
                    self.power = p
                    await asyncio.sleep(1)
                    fh.write(f"{f},{p},{self.sensor_speed}\n")
                    fh.flush()
                    await asyncio.sleep(1)
                    fh.write(f"{f},{p},{self.sensor_speed}\n")
                    fh.flush()
                    await asyncio.sleep(1)
    
    @property
    def frequency(self):
        f1 = self.pigpio.get_PWM_frequency(self.pin_enable1)
        f2 = self.pigpio.get_PWM_frequency(self.pin_enable2)
        return (f1+f2)/2
    
    @frequency.setter
    def frequency(self, value):
        self.pigpio.set_PWM_frequency(self.pin_enable1, value)
        self.pigpio.set_PWM_frequency(self.pin_enable2, value)   
    
    @property
    def power(self):
        return self._power
#         dc1 = self.pigpio.get_PWM_dutycycle(self.pin_enable1)
#         dc2 = self.pigpio.get_PWM_dutycycle(self.pin_enable2)
#         return (dc1+dc2)/2
    
    @power.setter
    def power(self, value):
        """power int: 0-255"""
        self._power = range_bound(value, 0, 255)
        self.pigpio.set_PWM_dutycycle(self.pin_enable1, self._power)
        self.pigpio.set_PWM_dutycycle(self.pin_enable2, self._power)
            
    def control(self, in1, in2, enable):
        self.pigpio.write(self.pin_input1, in1)
        self.pigpio.write(self.pin_input2, in2)
        self.pigpio.write(self.pin_enable1, enable)
        self.pigpio.write(self.pin_enable2, enable)
                
    async def speed_regulator(self):
        tolerance = 0.01
        while True:
            speed_diff = abs(self.velocity) - self.sensor_speed
            if abs(speed_diff) >= tolerance:
                power_delta = int(range_bound(speed_diff/tolerance, -5, 5))
                self.log.info(f"Speed: requested: {abs(self.velocity):.2f}; sensor: {self.sensor_speed:.2f}; power: {self.power}; delta: {power_delta}")
                self.power += power_delta
            await asyncio.sleep(settings.wheel_speed_regulator_interval)
    
    @property
    def sensor_speed(self):
        if self.sensor_last_tick is not None:
            last_tick_diff_ms = tickDiff(self.sensor_last_tick, self.pigpio.get_current_tick())
            if last_tick_diff_ms > 1000000: # 1/10th second
                return 0
        return self._sensor_speed
    
    @property
    def sensor_velocity(self):
        self.sensor_speed * np.sign(self._velocity)
             
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, value):
        """value in m/s"""
        # todo: handle minimum velocity
        self.log.info(f"Set velocity: {value}")
        self._velocity = value
        if value is None: # coast on brake
            self.control(0, 0, 0)
            self.power = 0
        elif value > 0:
            self.control(0, 1, 1)
        elif value < 0:
            self.control(1, 0, 1)
        else: # hard brake
            self.control(1, 1, 0)
            self.power = 0
            
    def accelerate(self, delta = 1):
        self.velocity += delta
        
class MotorPair(object):
    def __init__(self, loop):
        self.m1 = Motor("m1", 
            settings.gpio_wheel_motor_left_enable_1,
            settings.gpio_wheel_motor_left_enable_2,
            settings.gpio_wheel_motor_left_input_1,
            settings.gpio_wheel_motor_left_input_2,
            settings.gpio_wheel_sensor_left,
            loop)
        
        self.m2 = Motor("m2", 
            settings.gpio_wheel_motor_right_enable_1,
            settings.gpio_wheel_motor_right_enable_2,
            settings.gpio_wheel_motor_right_input_1,
            settings.gpio_wheel_motor_right_input_2,
            settings.gpio_wheel_sensor_right,
            loop)
        
        loop.create_task(self.m1.speed_regulator())
        loop.create_task(self.m2.speed_regulator())
              
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
    
    log = logging.getLogger("motor test")
    
    async def input(s):
        print(s)
        return await loop.run_in_executor(None, sys.stdin.readline)
    
    commands = [
        ("quit", None),
        ("stop", lambda mp: mp.set_velocity(0)),
        ("forward", lambda mp: mp.set_velocity(.35)),
        ("backward", lambda mp: mp.set_velocity(-.35)),
        ("rotate left", lambda mp: mp.rotate_left()),
        ("rotate right", lambda mp: mp.rotate_right()),
        ("bear left", lambda mp: mp.bear_left(.5)),
        ("bear right", lambda mp: mp.bear_right(.5)),
        ("bear right", lambda mp: mp.accelerate(.1)),
    ]
    
    mp = MotorPair(loop=loop)
    mp.set_velocity(0)
    
    for i, c in enumerate(commands):
        print(f"{i}) {c[0]}")

    while True:
        i_str = await input("Press Enter to continue...")
        i = int(i_str)
        if i == 0:
            break
        commands[i][1](mp)

    mp.set_velocity(0)

def main():
    from robot.utility.logging import console_log_handler
    logger = logging.getLogger('')
    logger.addHandler(console_log_handler)
    logger.setLevel(logging.DEBUG)
    
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(motor_test_routines(loop))
    
#     m1 = Motor("m1", 
#             settings.gpio_wheel_motor_left_enable_1,
#             settings.gpio_wheel_motor_left_enable_2,
#             settings.gpio_wheel_motor_left_input_1,
#             settings.gpio_wheel_motor_left_input_2,
#             settings.gpio_wheel_sensor_left,
#             loop)
#     loop.run_until_complete(m1.calibrate())
    
    


if __name__ == "__main__":
    main()
