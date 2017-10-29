from subprocess import check_output
from re import findall
from pathlib import Path
import psutil

from robot.utility.logger import Logger
log = Logger("Main").get_log()

class SystemInfo(object):
    log = Logger("SystemInfo").get_log()

    def cpu_temperature(self):
        p = Path("/sys/class/thermal/thermal_zone0/temp")
        if p.exists():
            with p.open() as f:
                return float(f.read().strip())/1000
        return None

    def gpu_temperature(self):
        p = Path('/opt/vc/bin/vcgencmd')
        if p.exists():
            out = check_output(['/opt/vc/bin/vcgencmd','measure_temp'])
            matches = findall("temp=(.*)'C", out.decode("utf8"))
            if matches:
                return float(matches[0])
        return None

    def core_voltage(self):
        p = Path('/opt/vc/bin/vcgencmd')
        if p.exists():
            out = check_output(['/opt/vc/bin/vcgencmd','measure_volts'])
            matches = findall("volt=(.*)V", out.decode("utf8"))
            if matches:
                return float(matches[0])
        return None


    def cpu_load(self):
        """
        Returns the cpu load as a value from the interval [0.0, 1.0]
        """
        INTERVAL = 0.1
        load = psutil.cpu_percent(interval=INTERVAL)
        return load
        

def main():
    s = SystemInfo()
    print(s.cpu_temperature())
    print(s.gpu_temperature())
    print(s.core_voltage())
    print(s.cpu_load())

if __name__ == "__main__":
    #import ptvsd
    #ptvsd.enable_attach(secret = 'rfvgy7', address = ('0.0.0.0', 8080))
    #ptvsd.wait_for_attach()
    main()
