'''
Created on 28 Oct 2017

@author: blair
'''
import os

if os.name == "nt":
    import Pyro4
    systeminfo_instance = Pyro4.Proxy("PYRONAME:robot.hardware.system.SystemInfo")
else:
    from robot.hardware.system import SystemInfo
    systeminfo_instance = SystemInfo()