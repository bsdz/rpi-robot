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
    log = Logger("AutoPilot").get_log()
    
    def __init__(self):
        self.log.info('initialize..')
        self.motor_pair = MotorPair()
        self.servo_pair = ServoPair()
        self.ultrasonic = Ultrasonic()
        self.measure_queue = Queue()
        self.drive_queue = Queue()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.log.info('cleaning up..')
        self.quit()

    def driver_queue_worker(self):
        self.log.info('starting...')
        while True:
            try:
                instruction = self.drive_queue.get()
                self.log.debug("processing instruction %s" % (instruction))
                self.drive_queue.task_done()
                if instruction == "quit":
                    self.motor_pair.set_velocity(0)
                    break
                elif instruction == "brake":
                    self.motor_pair.set_velocity(0)
                elif instruction == "forward":
                    self.motor_pair.set_velocity(30)
                elif instruction == "rotate":
                    self.motor_pair.set_velocity(0)
                    self.motor_pair.bear_left(30)

            except Exception, ex:
                self.log.error("exception: %s; %s" % (ex, sys.exc_info()[0]))
            except:
                self.log.error("unexpected error: %s" % (sys.exc_info()[0]))

        self.log.info('finished')

    def measurer_queue_worker(self):
        self.log.info('starting...')
        while True:
            try:
                instruction = self.measure_queue.get()
                self.log.debug("processing instruction %s" % (instruction))
                self.measure_queue.task_done()
                if instruction == "quit":
                    break
                elif instruction == "start":
                    weight_threshold = 0
                    last_instruction = None
                    while self.measure_queue.empty():  
                        distance = self.ultrasonic.measure()
                        #self.log.debug("Measured distance %s; threshold: %s" % (distance, weight_threshold))
                        if distance < 0.4 and weight_threshold > -10:
                            weight_threshold -= 1
                        elif distance >= 0.4 and weight_threshold < 10:
                            weight_threshold += 1

                        if weight_threshold == -10:
                            instruction = "rotate"
                        elif weight_threshold == 10:
                            instruction = "forward"
                        
                        if instruction and (not last_instruction or last_instruction != instruction):
                            self.log.debug("sending drive queue instruction: %s" % instruction)
                            self.drive_queue.put(instruction) 
                            last_instruction = instruction

                        sleep(0.01)
                elif instruction == "stop":
                    pass
            except Exception, ex:
                self.log.error("exception: %s; %s" % (ex, sys.exc_info()[0]))
            except:
                self.log.error("unexpected error: %s" % (sys.exc_info()[0]))

        self.log.info('finished')

    def control_worker(self):
        self.log.info('starting...')
        while True:
            try:
                instruction = self.drive_queue.get()
                self.log.debug("processing instruction %s" % (instruction))
                self.drive_queue.task_done()
                if instruction == "quit":
                    break

            except Exception, ex:
                self.log.error("exception: %s; %s" % (ex, sys.exc_info()[0]))
            except:
                self.log.error("unexpected error: %s" % (sys.exc_info()[0]))

        self.log.info('finished')

    def start(self):
        self.log.debug('starting autopilot..')

        self.measurer_queue_thread = Thread(name="MeasurerQueueThread", target=self.measurer_queue_worker)
        self.measurer_queue_thread.setDaemon(True)
        self.measurer_queue_thread.start()

        self.driver_queue_thread = Thread(name="DriverQueueThread", target=self.driver_queue_worker)
        self.driver_queue_thread.setDaemon(True)
        self.driver_queue_thread.start()

        self.servo_pair.center()
        self.measure_queue.put("start")
        self.drive_queue.put("forward")

    def stop(self):
        self.measure_queue.put("stop")
        self.drive_queue.put("brake")

    def quit(self):
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
        raw_input("Press any key to stop.")
        ap.stop()

