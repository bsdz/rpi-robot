import os

haar_cascade_dir = r"D:\Projects\opencv\data\haarcascades" if os.name == 'nt' else r"/usr/local/share/OpenCV/haarcascades"
http_server_port = 8080
video_width = 640
video_height = 480
video_capture_device = 0 if os.name == "nt" else -1
video_source = "server_mjpeg_stream"


gpio_wheel_motor_left_enable_1 = 7
gpio_wheel_motor_left_enable_2 = 11
gpio_wheel_motor_left_input_1 = 13
gpio_wheel_motor_left_input_2 = 15

gpio_wheel_motor_right_enable_1 = 12
gpio_wheel_motor_right_enable_2 = 16
gpio_wheel_motor_right_input_1 = 18
gpio_wheel_motor_right_input_2 = 22

gpio_camera_servo_horizontal = 8 
gpio_camera_servo_vertical = 7

gpio_ultrasonic_trigger = 21
gpio_ultrasonic_echo = 19