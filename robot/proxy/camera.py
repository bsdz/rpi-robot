'''
Created on 28 Oct 2017

@author: blair
'''
import os
import robot.settings as settings

if os.name == "nt":
    import Pyro4
    systeminfo_instance = Pyro4.Proxy(f"PYRONAME:{settings.rpc_ns_camera_uri}@{settings.rpc_ip_address}:{settings.rpc_ns_ip_port}")
else:
    from robot.hardware.camera import Camera
    camera_instance = Camera()
    
if __name__ == "__main__":
    s = camera_instance
    print(s.read())