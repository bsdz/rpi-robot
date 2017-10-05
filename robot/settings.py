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

pigpio_server = "192.168.0.34" if os.name == "nt" else None

gpio_wheel_motor_left_enable_1 = 7 # pin number
gpio_wheel_motor_left_enable_2 = 11 # pin number
gpio_wheel_motor_left_input_1 = 13 # pin number
gpio_wheel_motor_left_input_2 = 15 # pin number

gpio_wheel_motor_right_enable_1 = 12 # pin number
gpio_wheel_motor_right_enable_2 = 16 # pin number
gpio_wheel_motor_right_input_1 = 18 # pin number
gpio_wheel_motor_right_input_2 = 22 # pin number

gpio_camera_servo_horizontal = 8 # gpio number 
gpio_camera_servo_vertical = 7 # gpio number

gpio_ultrasonic_trigger = 21 # pin number
gpio_ultrasonic_echo = 19 # pin number