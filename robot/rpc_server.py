#import time

import Pyro4.naming

import robot.settings as settings
from robot.hardware.system import SystemInfo


def main():
    Pyro4.config.SERVERTYPE = "multiplex"
    Pyro4.config.POLLTIMEOUT = 3

    nsUri, nsDaemon, bcServer = Pyro4.naming.startNS(
        host=settings.rpc_ip_address, 
        port=settings.rpc_ns_ip_port, 
        enableBroadcast=False)
    daemon = Pyro4.Daemon(
        host=settings.rpc_ip_address, 
        port=settings.rpc_ip_port)

    ExposedSystemInfo = Pyro4.expose(SystemInfo)
    uri_SystemInfo = daemon.register(ExposedSystemInfo)
    nsDaemon.nameserver.register(settings.rpc_ns_systeminfo_uri, uri_SystemInfo)

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
    main()
