

Requirements

Hardware

Video camera


Software
Create virtualenv with python 3.6
Install python packages in requirements.txt file.

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
