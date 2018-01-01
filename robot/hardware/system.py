'''system board info

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
from subprocess import check_output
from re import findall
from pathlib import Path
import psutil
import logging

class SystemInfo(object):
    def __init__(self):
        self.log = logging.getLogger("system_info")

    def cpu_temperature(self):
        p = Path("/sys/class/thermal/thermal_zone0/temp")
        if p.exists():
            with p.open() as f:
                return float(f.read().strip())/1000
        return None
    
    async def async_cpu_temperature(self):
        return await self.loop.run_in_executor(None, self.cpu_temperature)

    def gpu_temperature(self):
        p = Path('/opt/vc/bin/vcgencmd')
        if p.exists():
            out = check_output(['/opt/vc/bin/vcgencmd','measure_temp'])
            matches = findall("temp=(.*)'C", out.decode("utf8"))
            if matches:
                return float(matches[0])
        return None
    
    async def async_gpu_temperature(self):
        return await self.loop.run_in_executor(None, self.gpu_temperature)

    def core_voltage(self):
        p = Path('/opt/vc/bin/vcgencmd')
        if p.exists():
            out = check_output(['/opt/vc/bin/vcgencmd','measure_volts'])
            matches = findall("volt=(.*)V", out.decode("utf8"))
            if matches:
                return float(matches[0])
        return None

    async def async_core_voltage(self):
        return await self.loop.run_in_executor(None, self.core_voltage)

    def cpu_load(self):
        """
        Returns the cpu load as a value from the interval [0.0, 1.0]
        """
        INTERVAL = 0.1
        load = psutil.cpu_percent(interval=INTERVAL)
        return load

    async def async_cpu_load(self):
        return await self.loop.run_in_executor(None, self.cpu_load)

def main():
    from robot.utility.logging import console_log_handler
    logger = logging.getLogger('')
    logger.addHandler(console_log_handler)
    logger.setLevel(logging.DEBUG)
    
    s = SystemInfo()
    logger.info(f'cpu temp: {s.cpu_temperature()}')
    logger.info(f'gpu temp: {s.gpu_temperature()}')
    logger.info(f'core volts: {s.core_voltage()}')
    logger.info(f'cpu load: {s.cpu_load()}')

if __name__ == "__main__":
    main()
