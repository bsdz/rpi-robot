'''rpc server for remote development

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''

import logging

import Pyro4.naming

import robot.settings as settings
from robot.hardware.system import SystemInfo
from robot.hardware.camera import Camera

log = logging.getLogger(f'rpc_server')

def main():
    Pyro4.config.SERVERTYPE = "multiplex"
    Pyro4.config.POLLTIMEOUT = 3
    Pyro4.config.SERIALIZERS_ACCEPTED.add("pickle")

    nsUri, nsDaemon, bcServer = Pyro4.naming.startNS(
        host=settings.rpc_ip_address, 
        port=settings.rpc_ns_ip_port, 
        enableBroadcast=False)
    daemon = Pyro4.Daemon(
        host=settings.rpc_ip_address, 
        port=settings.rpc_ip_port)

    systeminfo_uri = daemon.register(Pyro4.expose(SystemInfo))
    nsDaemon.nameserver.register(settings.rpc_ns_systeminfo_uri, systeminfo_uri)
    
    camera_uri = daemon.register(Pyro4.expose(Camera))
    nsDaemon.nameserver.register(settings.rpc_ns_camera_uri, camera_uri)

    daemon.combine(nsDaemon)

    def loopcondition():
        #print(time.asctime(), "Waiting for requests...")
        return True
    
    print(f"nameserver listening on: {settings.rpc_ip_address}:{settings.rpc_ns_ip_port}")
    print(f"rpc server listening on: {settings.robot_ip_address}:{settings.rpc_ip_port}")
    daemon.requestLoop(loopcondition)

    nsDaemon.close()
    daemon.close()


if __name__ == "__main__":
    from robot.utility.logging import console_log_handler
    logger = logging.getLogger('')
    logger.addHandler(console_log_handler)
    logger.setLevel(logging.DEBUG)
    
    main()
