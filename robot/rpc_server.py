import time

import Pyro4.core
import Pyro4.naming
import Pyro4.socketutil

#import Pyro4

import robot.settings as settings
from robot.hardware.system import SystemInfo

Pyro4.config.SERVERTYPE = "multiplex"
Pyro4.config.POLLTIMEOUT = 3

nameserverUri, nameserverDaemon, broadcastServer = Pyro4.naming.startNS(host=settings.robot_ip_address)

daemon = Pyro4.Daemon(host=settings.robot_ip_address)


ExposedSystemInfo = Pyro4.expose(SystemInfo)
uri_SystemInfo = daemon.register(ExposedSystemInfo)
nameserverDaemon.nameserver.register("robot.hardware.system.SystemInfo", uri_SystemInfo)

daemon.combine(nameserverDaemon)
daemon.combine(broadcastServer)

def loopcondition():
    print(time.asctime(), "Waiting for requests...")
    return True

daemon.requestLoop(loopcondition)

nameserverDaemon.close()
broadcastServer.close()
daemon.close()
