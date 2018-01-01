'''GPS sensor

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''

import logging
import asyncio

import serial_asyncio
from micropyGPS import MicropyGPS

import robot.settings as settings

class GPSTextStreamReader(asyncio.Protocol):
    def __init__(self, gps_parser):
        self.log = logging.getLogger('gps_stream_reader')
        self.gps_parser = gps_parser

    def connection_made(self, transport):
        self.transport = transport
        self.log.info('port opened', transport)

    def data_received(self, data):
        for c in data:
            self.gps_parser.update(chr(c))

    def connection_lost(self, exc):
        self.log.info('port closed')
        self.transport.loop.stop()

async def create_gps_worker(loop, gps_parser):
    srv = await serial_asyncio.create_serial_connection(loop, lambda: GPSTextStreamReader(gps_parser), 
                        settings.gps_device_tty_path, baudrate=settings.gps_device_tty_baudrate)
    return srv


async def gps_echo(gps):
    while True:
        if gps.fix_type == 1:
            print("no fix")
        else:
            print(f'fix: {gps.fix_type}D; measured: {gps.latitude}, {gps.longitude}; sateliites: {gps.satellites_used}')
        await asyncio.sleep(1)

def main():
    loop = asyncio.get_event_loop()
    gps_parser = MicropyGPS()
    #gps_reader = serial_asyncio.create_serial_connection(loop, lambda: GPSTextStreamReader(gps_parser), '/dev/rfcomm0', baudrate=9600)
    loop.create_task(gps_echo(gps_parser))
    loop.run_until_complete(create_gps_worker(loop, gps_parser))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
