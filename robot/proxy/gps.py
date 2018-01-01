'''gps remote hardware proxy

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
    GPS = type("GPS", (object,), {})
    GPS.async_fix_type = lambda self: client['gps_fix_type']()
    GPS.async_latitude = lambda self: client['gps_latitude']()
    GPS.async_longitude = lambda self: client['gps_longitude']()
    GPS.async_satellites_used = lambda self: client['gps_satellites_used']()
    gps_instance = GPS()
else:    
    from robot.hardware.gps import GPS, create_gps_worker
    
    loop = asyncio.get_event_loop()
    gps_instance = GPS()
    loop.run_until_complete(create_gps_worker(loop, gps_instance.micropy_gps))

async def gps_echo(gps_instance):
    while True:
        
        fix_type, latitude, longitude, satellites_used = await asyncio.gather(
            gps_instance.async_fix_type(),
            gps_instance.async_latitude(),
            gps_instance.async_longitude(),
            gps_instance.async_satellites_used(),
        )
        
        if fix_type == 1:
            print("no fix")
        else:
            print(f'fix: {fix_type}D; measured: {latitude}, {longitude}; sateliites: {satellites_used}')
        await asyncio.sleep(1)
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    s = gps_instance
    loop.run_until_complete(gps_echo(s))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
