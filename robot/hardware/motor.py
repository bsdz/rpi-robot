import robot.settings as settings
from robot.hardware.gpio import pigpio_instance, INPUT, EITHER_EDGE, tickDiff
from robot.utility.logger import Logger
log = Logger("Main").get_log()

PI = 3.1415926

class Motor(object): # 7,11,13,15
    log = Logger("Motor").get_log()

    def __init__(self, name, pin_enable1, pin_enable2, pin_input1, pin_input2, pin_speedsensor):
        self.name = name
        self.pigpio = pigpio_instance
        
        self.pin_enable1 = pin_enable1
        self.pin_enable2 = pin_enable2
        self.pin_input1 = pin_input1
        self.pin_input2 = pin_input2
        self.pin_speedsensor = pin_speedsensor
        
        self.sensor_speed_meters_per_second = None
        self.sensor_last_tick = None
        self.sensor_tick_interval_microseconds = None
        def _cbf(gpio, level, tick):
            if self.sensor_last_tick is not None:
                self.sensor_tick_interval_microseconds = tickDiff(self.sensor_last_tick, tick)
                self.sensor_speed_meters_per_second = 1000 * PI * settings.wheel_diameter_millimetres / self.sensor_tick_interval_microseconds / settings.wheel_sensor_notches
            self.sensor_last_tick = tick
        
        self.pigpio.set_mode(self.pin_speedsensor, INPUT)
        self.pigpio.callback(self.pin_speedsensor, EITHER_EDGE, _cbf)
        
        self.pwm_frequency = 40
        self.minimum_speed = 15
        self.maximum_speed = 100
        self.speed = 0
        self.direction = 0 # 1 ~ forward, 0 ~ stationary, -1 ~ backward       

    def enable(self, enable):
        self.pigpio.write(self.pin_enable1, 1 if enable else 0)
        self.pigpio.write(self.pin_enable2, 1 if enable else 0)
        if enable:
            self.pigpio.set_PWM_frequency(self.pin_enable1, self.pwm_frequency)
            self.pigpio.set_PWM_frequency(self.pin_enable2, self.pwm_frequency)
            self.pigpio.set_PWM_dutycycle(self.pin_enable1, self.speed)
            self.pigpio.set_PWM_dutycycle(self.pin_enable2, self.speed)
        else:      
            self.pigpio.set_PWM_dutycycle(self.pin_enable1, 0)
            self.pigpio.set_PWM_dutycycle(self.pin_enable2, 0)
            
    def control(self, in1, in2, speed = 90):
        if speed > 100: speed = self.maximum_speed
        if speed < 0: speed = 0
        self.speed = speed
        self.log.debug("motor %s set speed: %s; direction: %s" % (self.name, self.speed, self.direction))
        # override actual motor speed to avoid ineffective pwm duty cycle
        actual_motor_speed = self.minimum_speed if speed != 0 and speed < self.minimum_speed else speed		
        self.pigpio.write(self.pin_input1, in1)
        self.pigpio.write(self.pin_input2, in2)
        self.pigpio.set_PWM_dutycycle(self.pin_enable1, actual_motor_speed)
        self.pigpio.set_PWM_dutycycle(self.pin_enable2, actual_motor_speed)                                 
       
    def set_velocity(self, velocity=0, coast_on_brake=False):
        self.direction = (velocity > 0) - (velocity < 0)
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

    def get_velocity(self):
        return self.direction * self.speed

        
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
        
        self.m1.enable(True)
        self.m2.enable(True)
              
    def set_velocity(self, velocity):
        self.m1.set_velocity(velocity)
        self.m2.set_velocity(velocity)
        
    def accelerate(self, delta):
        self.m1.accelerate(delta)
        self.m2.accelerate(delta)
        
    def bear_left(self, delta=-1):
        self.m1.accelerate(-delta)
        self.m2.accelerate(delta)
        
    def bear_right(self, delta=-1):
        self.m1.accelerate(delta)
        self.m2.accelerate(-delta)        
        
    def rotate_left(self, rotate_speed = 50):
        self.m1.set_velocity(rotate_speed)
        self.m2.set_velocity(0)
        
    def rotate_right(self, rotate_speed = 50):
        self.m1.set_velocity(0)
        self.m2.set_velocity(rotate_speed)

def main():
    mp = MotorPair()
    input("Press Enter to continue...")
    
    log.info("forward")
    mp.set_velocity(40)
    input("Press Enter to continue...")

    log.info("backward")
    mp.set_velocity(-40)
    input("Press Enter to continue...")

    log.info("rotate left")
    mp.rotate_left()
    input("Press Enter to continue...")

    log.info("rotate right")
    mp.rotate_right()
    input("Press Enter to continue...")
    
    log.info("bear left")
    mp.set_velocity(50)
    input("Press Enter to continue...")
    mp.bear_left(10)
    input("Press Enter to continue...")
 
    log.info("bear left")
    mp.set_velocity(50)
    input("Press Enter to continue...")
    mp.bear_right(10)
    input("Press Enter to continue...")       
    
    log.info("accelerate test")
    mp.set_velocity(-50)
    for i in range(0,9):
        mp.accelerate(10)
        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
