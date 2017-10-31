'''camera remote hardware proxy

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import os
import robot.settings as settings

if os.name == "nt":
    import Pyro4
    Pyro4.config.SERIALIZER = 'pickle'
    camera_instance = Pyro4.Proxy(f"PYRONAME:{settings.rpc_ns_camera_uri}@{settings.rpc_ip_address}:{settings.rpc_ns_ip_port}")
else:
    from robot.hardware.camera import Camera
    camera_instance = Camera()
    
if __name__ == "__main__":
    s = camera_instance
    print(s.read())