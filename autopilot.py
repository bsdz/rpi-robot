#!/usr/bin/python

import sys
import signal
from time import sleep
from Queue import Queue
from threading import Thread

from motor import MotorPair
from servo import ServoPair
from ultrasonic import Ultrasonic

from logger import Logger
log = Logger("Main").get_log()

def signal_handler(signal, frame):
    log.info("SIGINT caught. Exiting gracefully")       
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class AutoPilot(object):
    log = Logger("Main").get_log()
    
    def __init__(self):
        self.log.info('autopilot: initialize..')
        self.motor_pair = MotorPair()
        self.servo_pair = ServoPair()
        self.ultrasonic = Ultrasonic()
        self.measure_queue = Queue()
        self.drive_queue = Queue()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.log.info('autopilot: cleaning up..')
        self.stop()

    def driver_queue_worker(self):
        self.log.info('starting driver queue worker...')
        while True:
            try:
                instruction = self.drive_queue.get()
                self.log.debug("DriverQueueWorker: processing instruction %s" % (instruction))
                self.drive_queue.task_done()
                if instruction == "quit":
                    self.motor_pair.set_velocity(0)
                    break
                elif instruction == "brake":
                    self.motor_pair.set_velocity(0)
                elif instruction == "forward":
                    self.motor_pair.set_velocity(50)
                elif instruction == "rotate":
                    self.motor_pair.set_velocity(0)
                    self.motor_pair.bear_left(40)

                """
                self.motor_pair.accelerate(10)
                self.motor_pair.accelerate(-10) 
                self.motor_pair.bear_left(-10)
                self.motor_pair.bear_right(-10)
                self.motor_pair.set_velocity(0)
                """
                    
            except Exception, ex:
                self.log.error("DriverQueueWorker: exception: %s" % (ex))
            except:
                self.log.error("DriverQueueWorker: unexpected error: %s" % (sys.exc_info()[0]))

    def measurer_queue_worker(self):
        self.log.info('starting measurer queue worker...')
        while True:
            try:
                instruction = self.measure_queue.get()
                self.log.debug("MeasurerQueueWorker: processing instruction %s" % (instruction))
                self.measure_queue.task_done()
                if instruction == "quit":
                    break
                elif instruction == "start":
                    while self.measure_queue.empty():  
                        # take measurements and act
                        distance = self.ultrasonic.measure()
                        self.log.debug("Measured distance %s" % (distance))
                        if distance < 0.4:
                            self.drive_queue.put("rotate") 
                        elif distance >= 0.4:
                            self.drive_queue.put("forward") 

                        sleep(0.01)
                elif instruction == "stop":
                    pass
            except Exception, ex:
                self.log.error("MeasurerQueueWorker: exception: %s" % (ex))
            except:
                self.log.error("MeasurerQueueWorker: unexpected error: %s" % (sys.exc_info()[0]))
            
    def start(self):
        self.log.debug('starting autopilot..')

        self.measurer_queue_thread = Thread(name="MeasurerQueueThread", target=self.measurer_queue_worker)
        self.measurer_queue_thread.setDaemon(True)
        self.measurer_queue_thread.start()

        self.driver_queue_thread = Thread(name="DriverQueueThread", target=self.driver_queue_worker)
        self.driver_queue_thread.setDaemon(True)
        self.driver_queue_thread.start()

        self.measure_queue.put("start")
        self.drive_queue.put("forward")

        while True:
            #res = self.radial_distance_scan()
            # choose max distance
            #target_dir = max(res, key=res.get)
            # rotate facing max distance
            # move forward while monitor distance until min distance reached
            sleep(1)

        """
            self.motor_pair.accelerate(10)
            self.motor_pair.accelerate(-10) 
            self.motor_pair.bear_left(-10)
            self.motor_pair.bear_right(-10)
            self.motor_pair.set_velocity(0)
        """

    def stop(self):
        self.measure_queue.put("quit")
        self.measurer_queue_thread.join()
        self.drive_queue.put("quit")
        self.driver_queue_thread.join()
    
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
        ap.stop()

