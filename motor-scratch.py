import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)

gpio.setup(7, gpio.OUT)  # m0 enable 1
gpio.setup(11, gpio.OUT) # m0 enable 2
gpio.setup(13, gpio.OUT) # m0 input 1
gpio.setup(15, gpio.OUT) # m0 input 2

gpio.output(7, True)
gpio.output(11, True)


pwm_frequency = 40

p7 = gpio.PWM(7, pwm_frequency)
p11 = gpio.PWM(11, pwm_frequency) 

s = 100
p7.start(s)
p11.start(s)


gpio.output(13, True)
gpio.output(15, False)


#p13 = gpio.PWM(13, pwm_frequency)
#p15 = gpio.PWM(15, pwm_frequency) 

#p13.start(90)
#p15.start(90)

raw_input("Press Enter to continue...")



gpio.output(7, False)
gpio.output(11, False)


gpio.cleanup()
