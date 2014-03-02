import time
from subprocess import check_output
from re import findall

from logger import Logger
log = Logger("Main").get_log()

class System(object):
    log = Logger("System").get_log()

    def __init__(self):
        pass

    def cpu_temperature(self):
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return float(f.read().strip())/1000

    def gpu_temperature(self):
        out = check_output(['/opt/vc/bin/vcgencmd','measure_temp'])
        matches = findall("temp=(.*)'C", out)
        return float(matches[0]) if matches else None

    def core_voltage(self): 
        out = check_output(['/opt/vc/bin/vcgencmd','measure_volts'])
        matches = findall("volt=(.*)V", out)
        return float(matches[0]) if matches else None

    def time_list(self):
        """
        Fetches a list of time units the cpu has spent in various modes
        Detailed explanation at http://www.linuxhowtos.org/System/procstat.htm
        """
        cpuStats = file("/proc/stat", "r").readline()
        columns = cpuStats.replace("cpu", "").split(" ")
        return map(int, filter(None, columns))

    def delta_time(self, interval):
        """
        Returns the difference of the cpu statistics returned by getTimeList
        that occurred in the given time delta
        """
        timeList1 = self.time_list()
        time.sleep(interval)
        timeList2 = self.time_list()
        return [(t2-t1) for t1, t2 in zip(timeList1, timeList2)]

    def cpu_load(self):
        """
        Returns the cpu load as a value from the interval [0.0, 1.0]
        """
        INTERVAL = 0.1
        dt = list(self.delta_time(INTERVAL))
        idle_time = float(dt[3])
        total_time = sum(dt)
        load = 1-(idle_time/total_time)
        return load
        

def main():
    s = System()
    print s.cpu_temperature()
    print s.gpu_temperature()
    print s.core_voltage()
    print s.cpu_load()

if __name__ == "__main__":
    #import ptvsd
    #ptvsd.enable_attach(secret = 'rfvgy7', address = ('0.0.0.0', 8080))
    #ptvsd.wait_for_attach()
    main()
