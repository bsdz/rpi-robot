#!/usr/bin/python

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import json
import sys
import traceback

from time import sleep
from queue import Queue
from threading import Thread

from robot.hardware.motor import MotorPair
from robot.hardware.servo import ServoPair
from robot.hardware.system import System
from robot.hardware.ultrasonic import Ultrasonic
from robot.autopilot import AutoPilot

from robot.utility.logger import Logger
log = Logger("Main").get_log()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate())
        #log.info(repr(self.request))
            

class WSHandler(tornado.websocket.WebSocketHandler):
    log = Logger("WSHandler").get_log()
    
    def initialize(self):
        self.status_update_queue = Queue()
        self.status_update_thread = Thread(name="StatusUpdateThread", target=self.status_update_worker)
        self.status_update_thread.setDaemon(True)
        self.status_update_thread.start()  

    def open(self):
        self.log.info('connection opened...')
        self.motor_pair = MotorPair()
        self.servo = ServoPair()
        self.ultrasonic = Ultrasonic()
        self.auto_pilot = AutoPilot()
            
        self.message_queue_thread = Thread(name="MessageQueueThread", target=self.message_queue_worker)
        self.message_queue_thread.setDaemon(True)
        self.message_queue_thread.start()

    def on_close(self):
        self.log.info('connection closed...')             

    def on_message(self, message):
        self.log.debug('received: %s' % (message))
        if message == "forward":
            self.motor_pair.accelerate(10)
        elif message == "backward":
            self.motor_pair.accelerate(-10) 
        elif message == "turnleft":
            self.motor_pair.bear_left(-10)
        elif message == "turnright":
            self.motor_pair.bear_right(-10)
        elif message == "brake":
            self.motor_pair.set_velocity(0)
        elif message == "panleft":
            self.servo.pan_left()
        elif message == "panright":
            self.servo.pan_right()
        elif message == "tiltup":
            self.servo.tilt_up()
        elif message == "tiltdown":
            self.servo.tilt_down()
        elif message == "center":
            self.servo.center()
        elif message == "autopiloton":
            self.auto_pilot.start()
            self.auto_pilot_on = True
        elif message == "autopilotoff":
            self.auto_pilot.stop()
            self.auto_pilot_on = False
        else:
            self.log.debug('unknown message received: %s' % (message))

        message = {
            "status": {
                "m1Speed": self.motor_pair.m1.get_velocity(),
                "m2Speed": self.motor_pair.m2.get_velocity(),
                "servoHoriz": self.servo.horizontal.current,
                "servoVert": self.servo.vertical.current,
            }
        }
        self.status_update_queue.put(json.dumps(message))
        
    def status_update_worker(self):
        log.info('starting..')
        si = System()
        while True:
            try:
                message = {
                    "status": {
                        "cpuTemp": si.cpu_temperature(),
                        "gpuTemp": si.gpu_temperature(),
                        "coreVolt": si.core_voltage(),
                        "cpuLoad": 100*si.cpu_load()
                    }
                }
                if not self.auto_pilot.is_active:
                    message["status"]["forwardDistance"] = self.ultrasonic.measure()
                self.status_update_queue.put(json.dumps(message))  
                sleep(1) 
            except:
                ex = sys.exc_info()
                self.log.error("exception: %s; %s; %s" % (ex[0], ex[1], traceback.format_tb(ex[2])))
        
    def message_queue_worker(self):
        log.info('starting..')
        while True:
            try:
                item = self.status_update_queue.get()
                self.log.debug("writing item %s" % (item))
                self.write_message(item, binary=False)
                self.status_update_queue.task_done()       
            except:
                ex = sys.exc_info()
                self.log.error("exception: %s; %s; %s" % (ex[0], ex[1], traceback.format_tb(ex[2])))

def start_web_application():
    application = tornado.web.Application([
        (r'/ws', WSHandler),
        (r'/', MainHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
    ])

    application.listen(9093)    
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    start_web_application()
    
 
