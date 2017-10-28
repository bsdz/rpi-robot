from robot.hardware.system import SystemInfo
import Pyro4

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()

ExposedSystemInfo = Pyro4.expose(SystemInfo)
uri_SystemInfo = daemon.register(ExposedSystemInfo)
ns.register("robot.hardware.system.SystemInfo", uri_SystemInfo)

daemon.requestLoop()