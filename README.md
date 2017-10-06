Requirements

# Hardware #

* Video camera
* Ultrasonic sensor
* 2 x Servos
* 2 x Motors + Controller + Chasis
* Speed sensor
* Microswitches

# Software # 

* Python 3.6
* Python packages in requirements.txt.
* pigpio - see https://github.com/joan2937/pigpio/ and http://abyz.co.uk/rpi/pigpio/download.html

# Configuration #

* Build robot according to specification.
* Create virtualenv with python 3.6 (uses async).
* Install python packages in requirements.txt file.
* In /etc/rc.local add:
	chown root.gpio /dev/gpiomem
	chmod g+rw /dev/gpiomem
	pigpiod

# Running #

* Activate virtualenv
* Go to cloned code folder
* python -m robot.robot_server main
