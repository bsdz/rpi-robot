'''system board remote hardware proxy

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
    SystemInfo = type("SystemInfo", (object,), {})
    SystemInfo.async_cpu_temperature = lambda self: client['system_info_cpu_temperature']()
    SystemInfo.async_gpu_temperature = lambda self: client['system_info_gpu_temperature']()
    SystemInfo.async_core_voltage = lambda self: client['system_info_core_voltage']()
    SystemInfo.async_cpu_load = lambda self: client['system_info_cpu_load']()
    systeminfo_instance = SystemInfo()
else:
    from robot.hardware.system import SystemInfo
    systeminfo_instance = SystemInfo()
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    s = systeminfo_instance
    print(loop.run_until_complete(s.async_cpu_temperature()))
    print(loop.run_until_complete(s.async_gpu_temperature()))
    print(loop.run_until_complete(s.async_core_voltage()))
    print(loop.run_until_complete(s.async_cpu_load()))
