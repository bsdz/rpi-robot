'''
Created on 28 Oct 2017

@author: blair
'''
import os
import robot.settings as settings

if os.name == "nt":
    import Pyro4
    systeminfo_instance = Pyro4.Proxy(f"PYRONAME:{settings.rpc_ns_systeminfo_uri}@{settings.rpc_ip_address}:{settings.rpc_ns_ip_port}")
else:
    from robot.hardware.system import SystemInfo
    systeminfo_instance = SystemInfo()
    
if __name__ == "__main__":
    s = systeminfo_instance
    print(s.cpu_temperature())
    print(s.gpu_temperature())
    print(s.core_voltage())
    print(s.cpu_load())