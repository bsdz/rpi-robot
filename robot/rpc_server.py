'''rpc server for remote development

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''

import logging

import asyncio
from aiohttp import web
from aiohttp_xmlrpc import handler

import robot.settings as settings
from robot.hardware.system import SystemInfo
from robot.hardware.camera import Camera
from robot.hardware.gps import GPS, create_gps_worker
import robot.utility.aiohttp_xmlrpc_helpers  # @UnusedImport

log = logging.getLogger(__name__)

camera_instance = Camera()
systeminfo_instance = SystemInfo()
gps_instance = GPS()

class XMLRPCExample(handler.XMLRPCView):

    def rpc_camera_read(self):
        return camera_instance.read()

    def rpc_system_info_cpu_temperature(self):
        return systeminfo_instance.cpu_temperature()

    def rpc_system_info_gpu_temperature(self):
        return systeminfo_instance.gpu_temperature()

    def rpc_system_info_core_voltage(self):
        return systeminfo_instance.core_voltage()

    def rpc_system_info_cpu_load(self):
        return systeminfo_instance.cpu_load()

    def rpc_gps_fix_type(self):
        return gps_instance.fix_type()

    def rpc_gps_latitude(self):
        return gps_instance.latitude()
    
    def rpc_gps_longitude(self):
        return gps_instance.longitude()
    
    def rpc_gps_satellites_used(self):
        return gps_instance.satellites_used()
        
def main():

    app = web.Application()
    app.router.add_route('*', '/', XMLRPCExample)

    loop = asyncio.get_event_loop()

    loop.create_task(create_gps_worker(loop, gps_instance.micropy_gps))
    
    srv = loop.create_server(app.make_handler(), 
        settings.rpc_ip_address, 
        settings.rpc_ip_port)

    log.info(f"rpc server listening on: {settings.rpc_ip_address}:{settings.rpc_ip_port}")

    loop.run_until_complete(srv)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    from robot.utility.logging import console_log_handler
    logger = logging.getLogger('')
    logger.addHandler(console_log_handler)
    logger.setLevel(logging.DEBUG)

    logging.getLogger('aiohttp_xmlrpc').setLevel(logging.INFO)
    
    main()






