

Requirements

Hardware

Video camera


Software
Create virtualenv with python 3.6
Install python packages in requirements.txt file.

Install v4l2loopback for video.
* Build kernel as in https://www.raspberrypi.org/documentation/linux/kernel/building.md
* Build v4l2loopback as in https://github.com/umlaeute/v4l2loopback

Alternative to v4l2loopback
Install uv4l for video.
Install uv4l as in https://github.com/weiss19ja/amos-ss16-proj2/wiki/Videostream#streaming-video-with-uv4l-mmal and https://www.linux-projects.org/uv4l/installation/

Install pigpio
* Build as in https://github.com/joan2937/pigpio/ and http://abyz.co.uk/rpi/pigpio/download.html

Permissions to gpio
sudo chown root.gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem


Running
sudo bash
activate virtualenv
got to cloned code folder
python -m robot.control --register 
