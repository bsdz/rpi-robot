'''autopilot: due for a rewrite
rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import sys
import traceback
import signal
import logging
from time import sleep
from queue import Queue
from threading import Thread

from robot.hardware.motor import MotorPair
from robot.hardware.servo import ServoPair
from robot.hardware.ultrasonic import Ultrasonic

log = logging.getLogger('autopilot').addHandler(logging.NullHandler())

def signal_handler(signal, frame):
    log.info("SIGINT caught. Exiting gracefully")       
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class AutoPilot(object):
    log = Logger("AutoPilot").get_log()
    
    def __init__(self):
        self.log.info('initialize..')

        self.motor_pair = MotorPair()
        self.servo_pair = ServoPair()
        self.ultrasonic = Ultrasonic()
        
        self.is_active = False

        self.safe_to_proceed = False

        self.measure_queue = Queue()
        self.measurer_queue_thread = Thread(name="MeasurerQueueThread", target=self.measurer_queue_worker)
        self.measurer_queue_thread.setDaemon(True)
        self.measurer_queue_thread.start()

        self.drive_queue = Queue()
        self.driver_queue_thread = Thread(name="DriverQueueThread", target=self.driver_queue_worker)
        self.driver_queue_thread.setDaemon(True)
        self.driver_queue_thread.start()

        self.control_queue = Queue()
        self.control_queue_thread = Thread(name="ControlQueueThread", target=self.control_queue_worker)
        self.control_queue_thread.setDaemon(True)
        self.control_queue_thread.start()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.log.info('cleaning up..')
        self.quit()

    def quit(self):
        self.measure_queue.put("quit")
        self.measurer_queue_thread.join()
        self.drive_queue.put("quit")
        self.driver_queue_thread.join()
        self.control_queue.put("quit")
        self.control_queue_thread.join()

    def start(self):
        self.log.debug('starting autopilot..')
        self.control_queue.put("start")
        self.is_active = True

    def stop(self):
        self.log.debug('stopping autopilot..')
        self.control_queue.put("stop")
        self.is_active = False

    def driver_queue_worker(self):
        self.log.info('starting..')
        last_instruction = None
        while True:
            try:
                instruction = self.drive_queue.get()
                if not last_instruction or last_instruction != instruction:
                    self.log.debug("processing instruction %s" % (instruction))
                    if instruction == "brake":
                        self.motor_pair.set_velocity(0)
                    elif instruction == "forward":
                        self.motor_pair.set_velocity(40)
                    elif instruction == "rotate":
                        self.motor_pair.set_velocity(0)
                        self.motor_pair.bear_left(40)
                    elif instruction == "quit":
                        self.motor_pair.set_velocity(0)
                        break
                last_instruction = instruction
                self.drive_queue.task_done()
            except:
                ex = sys.exc_info()
                self.log.error("exception: %s; %s; %s" % (ex[0], ex[1], traceback.format_tb(ex[2])))
        self.log.info('finished')

    def measurer_queue_worker(self):
        self.log.info('starting...')
        while True:
            try:
                instruction = self.measure_queue.get()
                self.log.debug("processing instruction %s" % (instruction))
                if instruction == "quit":
                    break
                elif instruction == "start":
                    weight_threshold = 0
                    last_instruction = None
                    while self.measure_queue.empty():  
                        distance = self.ultrasonic.measure()
                        self.log.debug("Measured distance %s; threshold: %s" % (distance, weight_threshold))
                        if distance < 0.4 and weight_threshold > -10:
                            weight_threshold -= 1
                        elif distance >= 0.4 and weight_threshold < 10:
                            weight_threshold += 1

                        if weight_threshold == -10:
                            self.safe_to_proceed = False
                        elif weight_threshold == 10:
                            self.safe_to_proceed = True

                        sleep(0.01)
                elif instruction == "stop":
                    pass
                self.measure_queue.task_done()
            except:
                ex = sys.exc_info()
                self.log.error("exception: %s; %s; %s" % (ex[0], ex[1], traceback.format_tb(ex[2])))
        self.log.info('finished')

    def control_queue_worker(self):
        self.log.info('starting...')
        while True: 
            try:
                instruction = self.control_queue.get()
                self.log.debug("processing instruction %s" % (instruction))
                if instruction == "quit":
                    break
                elif instruction == "start":
                    self.servo_pair.center()
                    self.measure_queue.put("start")
                    #self.drive_queue.put("forward")
                    while self.control_queue.empty():  
                        if self.safe_to_proceed:
                            self.drive_queue.put("forward")
                        else:
                            self.drive_queue.put("rotate")
                        sleep(0.1)
                elif instruction == "stop":
                    self.measure_queue.put("stop")
                    self.drive_queue.put("brake")
                self.control_queue.task_done()
            except:
                ex = sys.exc_info()
                self.log.error("exception: %s; %s; %s" % (ex[0], ex[1], traceback.format_tb(ex[2])))
        self.log.info('finished')

    def radial_distance_scan(self):
        self.log.debug('scanning radial distance..')

        res = {}
        center_position = self.servo_pair.horizontal.default_position()
        for i in (range(center_position - 60, center_position + 60)):
            sleep(0.01)
            self.servo_pair.horizontal.current_position(i)
            distance = self.ultrasonic.measure()
            res[i] = distance
        return res

if __name__ == "__main__":
    with AutoPilot() as ap:
        ap.start()
        while True:
            sleep(1)
        input("Press any key to stop.")
        ap.stop()

