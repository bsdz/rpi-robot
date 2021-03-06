'''settings

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''

import os

import robot

log_file = os.path.join(os.path.dirname(os.path.dirname(robot.__file__)), "robot.log")

haar_cascade_dir = r"D:\Projects\opencv\data\haarcascades" if os.name == 'nt' else r"/usr/local/share/OpenCV/haarcascades"
http_server_port = 8090
http_server_address = '0.0.0.0'
video_width = 640
video_height = 480
video_capture_device = 0 if os.name == "nt" else -1
video_source = "server_mjpeg_stream"
video_capture_sleep_seconds = 0.2

robot_ip_address = "192.168.0.36"

# remote dev
rpc_ip_address = robot_ip_address
rpc_ip_port = 9090

# gps
gps_device_tty_path = '/dev/rfcomm0'
gps_device_tty_baudrate = 9600

# GPIO pin numbers
#
gpio_wheel_motor_left_enable_1 = 4
gpio_wheel_motor_left_enable_2 = 17
gpio_wheel_motor_left_input_1 = 22
gpio_wheel_motor_left_input_2 = 27

gpio_wheel_motor_right_enable_1 = 18
gpio_wheel_motor_right_enable_2 = 23
gpio_wheel_motor_right_input_1 = 24
gpio_wheel_motor_right_input_2 = 25

gpio_wheel_sensor_left = 26
gpio_wheel_sensor_right = 19

gpio_camera_servo_horizontal = 8 
gpio_camera_servo_vertical = 7

gpio_ultrasonic_trigger = 9
gpio_ultrasonic_echo = 10

# hardware settings
#
camera_servo_horizontal_minimum = 550 
camera_servo_horizontal_maximum = 2050
camera_servo_horizontal_center = 1250

camera_servo_vertical_minimum = 830
camera_servo_vertical_maximum = 2300
camera_servo_vertical_center = 900

wheel_sensor_notches = 20
wheel_diameter_millimetres = 65
wheel_speed_regulator_interval = 0.01
