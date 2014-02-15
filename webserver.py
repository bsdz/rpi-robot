#!/usr/bin/python

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template

from time import sleep
from Queue import Queue
from threading import Thread

from motor import MotorPair
from servo import Servo
from system import System

from logger import Logger
log = Logger("Main").get_log()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate())
        
def status_update_worker(status_update_queue):
    log.info('starting status update worker...')
    si = System()
    while True:
        message = "Status: CPU Temp %s; GPU Temp %s; Volt: %s; CPU Load: %.2f%%" % (si.cpu_temperature(), si.gpu_temperature(), si.core_voltage(), 100*si.cpu_load())
        status_update_queue.put(message)  
        sleep(10) 
        
def message_queue_worker(status_update_queue, web_socket_handler):
    log.info('starting message queue worker...')
    while True:
        item = status_update_queue.get()
        web_socket_handler.write_message(item, binary=False)
        status_update_queue.task_done()       

class WSHandler(tornado.websocket.WebSocketHandler):
    log = Logger("Main").get_log()
    
    def initialize(self, status_update_queue):
        self.status_update_queue = status_update_queue

    def open(self):
        self.log.info('connection opened...')
        self.motor_pair = MotorPair()
        self.servo = Servo()
            
        self.message_queue_thread = Thread(target=message_queue_worker, args=(status_update_queue, self))
        self.message_queue_thread.setDaemon(True)
        self.message_queue_thread.start()  

    def on_message(self, message):
        self.log.debug('received: %s' % (message))
        if message == "forward":
            self.motor_pair.accelerate(10)
        if message == "backward":
            self.motor_pair.accelerate(-10) 
        if message == "turnleft":
            self.motor_pair.bear_left(0)
        if message == "turnright":
            self.motor_pair.bear_right(-50)
        if message == "brake":
            self.motor_pair.set_velocity(0)
        if message == "panleft":
            self.servo.pan_left()
        if message == "panright":
            self.servo.pan_right()
        if message == "tiltup":
            self.servo.tilt_up()
        if message == "tiltdown":
            self.servo.tilt_down()
        if message == "center":
            self.servo.center()

    def on_close(self):
        self.log.info('connection closed...')             

if __name__ == "__main__":

    status_update_queue = Queue()

    application = tornado.web.Application([
        (r'/ws', WSHandler, {"status_update_queue": status_update_queue}),
        (r'/', MainHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
    ])

    status_update_thread = Thread(target=status_update_worker, args=(status_update_queue,))
    status_update_thread.setDaemon(True)
    status_update_thread.start()  

    application.listen(9093)
    tornado.ioloop.IOLoop.instance().start()
 
