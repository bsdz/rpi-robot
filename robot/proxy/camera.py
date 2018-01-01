'''camera remote hardware proxy

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import asyncio
import os
import robot.settings as settings

if os.name == "nt":   
    import robot.utility.aiohttp_xmlrpc_helpers  # @UnusedImport
    from aiohttp_xmlrpc.client import ServerProxy
    
    client = ServerProxy(f"http://{settings.rpc_ip_address}:{settings.rpc_ip_port}/")
    Camera = type("Camera", (object,), {})
    Camera.async_read = lambda self: client['camera_read']()
    camera_instance = Camera()
else:
    from robot.hardware.camera import Camera
    camera_instance = Camera()
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    s = camera_instance
    print(loop.run_until_complete(s.async_read()))
