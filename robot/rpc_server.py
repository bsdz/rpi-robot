import time

import Pyro4.core
import Pyro4.naming
import Pyro4.socketutil

import robot.settings as settings
from robot.hardware.system import SystemInfo


def main():
    Pyro4.config.SERVERTYPE = "multiplex"
    Pyro4.config.POLLTIMEOUT = 3

    nsUri, nsDaemon, bcServer = Pyro4.naming.startNS(host=settings.robot_ip_address, port=9090, enableBroadcast=False)
    daemon = Pyro4.Daemon(host=settings.robot_ip_address)

    ExposedSystemInfo = Pyro4.expose(SystemInfo)
    uri_SystemInfo = daemon.register(ExposedSystemInfo)
    nsDaemon.nameserver.register("robot.hardware.system.SystemInfo", uri_SystemInfo)

    daemon.combine(nsDaemon)

    def loopcondition():
        print(time.asctime(), "Waiting for requests...")
        return True

    daemon.requestLoop(loopcondition)

    nsDaemon.close()
    daemon.close()


if __name__ == "__main__":
    main()
