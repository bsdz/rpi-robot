'''main robot server

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import cv2
import os
import json
import async_timeout
import asyncio
import logging
#from threading import Thread
#import time, uuid
from functools import partial

from aiohttp import web, WSMsgType, ClientError
import aiohttp_jinja2
import jinja2

import robot.settings as settings
from robot.proxy.system import systeminfo_instance
from robot.proxy.camera import camera_instance

from robot.hardware.motor import MotorPair
from robot.hardware.servo import ServoPair
from robot.hardware.ultrasonic import Ultrasonic
#from robot.autopilot import AutoPilot

log = logging.getLogger(f'robot_server')

class Hardware(object):
    def __init__(self, loop):
        self.motor_pair = MotorPair(loop)
        self.servo_pair = ServoPair()
        self.ultrasonic = Ultrasonic()
        #self.auto_pilot = AutoPilot()

class ImageCaptureData(object):
    def __init__(self):
        self.count = 0
        self.face_detected = False

class SyncObjects(object):
    def __init__(self, loop):
        self.loop = loop
        self.allow_camera_capture = asyncio.Semaphore(value=0, loop=loop)
        self.client_log_message_queue = asyncio.Queue(loop=loop)
        self.client_image_queue = asyncio.Queue(maxsize=1, loop=loop)
        self.client_image_queue_lock = asyncio.Lock(loop=loop)
        self.hardware_command_queue = asyncio.Queue(loop=loop)

        self.image_capture_data = ImageCaptureData()
        self.hardware = Hardware(loop=loop)

async def camera_detect_worker(sync_objects):
    face_cascade = cv2.CascadeClassifier(os.path.join(settings.haar_cascade_dir, "haarcascade_frontalface_alt.xml"))
    eye_cascade = cv2.CascadeClassifier(os.path.join(settings.haar_cascade_dir, "haarcascade_eye.xml"))
    smile_cascade = cv2.CascadeClassifier(os.path.join(settings.haar_cascade_dir, "haarcascade_smile.xml"))
    
    await sync_objects.allow_camera_capture.acquire()
    log.info("Capturing camera...")
    await sync_objects.client_log_message_queue.put("Server capturing camera")
    
    while True:
        success, image = camera_instance.read()
        if success:
            #cv2.imwrite(fr'sample-{sync_objects.image_capture_data.count}.png',image)
            sync_objects.image_capture_data.count += 1
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,
                minNeighbors=8,
                minSize=(55, 55),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            if not list(faces):
                sync_objects.image_capture_data.face_detected = False
                
            for (x, y, w, h) in faces:
                sync_objects.image_capture_data.face_detected = True
                
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = image[y:y+h, x:x+w]
         
                smiles = smile_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.7,
                    minNeighbors=22,
                    minSize=(25, 25),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
         
                for (x, y, w, h) in smiles:
                    cv2.putText(image,"Smile detected", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                    cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)
            
                eyes = eye_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor= 1.1,
                    minNeighbors=3,
                    minSize=(5, 5),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                
                for (x, y, w, h) in eyes:
                    cv2.rectangle(roi_color, (x, y), (x+w, y+h), (0, 255, 0), 1)
            
                
            with (await sync_objects.client_image_queue_lock):
                image_jpeg_bytes = cv2.imencode('.jpg', image)[1].tobytes()
                if sync_objects.client_image_queue.full():
                    sync_objects.client_image_queue.get_nowait()
                sync_objects.client_image_queue.put_nowait(image_jpeg_bytes)
        
        await asyncio.sleep(settings.video_capture_sleep_seconds)

@aiohttp_jinja2.template('index.html')
async def index(sync_objects, request):
    if settings.video_source == "server_mjpeg_stream":
        sync_objects.allow_camera_capture.release()
    return dict({"video_source": settings.video_source})


async def video_feed(sync_objects, request, timeout=10):
    """Stream a stream to aiohttp web response."""
    response = web.StreamResponse()
    response.content_type = 'multipart/x-mixed-replace;boundary=ffserver'
    await response.prepare(request)

    try:
        while True:
            with async_timeout.timeout(timeout, loop=sync_objects.loop):
                data = await sync_objects.client_image_queue.get()

            if not data:
                await response.write_eof()
                break

            data2 =  b'--ffserver\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n'

            response.write(data2)

    except (asyncio.TimeoutError, ClientError):
        # Something went wrong fetching data, close connection gracefully
        await response.write_eof()

    except asyncio.CancelledError:
        # The user closed the connection
        pass



async def system_info_websocket_heartbeat(sync_objects, ws):
    while True:
        message = {
            "status": {
                "CPU Temp": systeminfo_instance.cpu_temperature(),
                "GPU Temp": systeminfo_instance.gpu_temperature(),
                "Core Volt": systeminfo_instance.core_voltage(),
                "CPU Load": systeminfo_instance.cpu_load(),
                "Images #": sync_objects.image_capture_data.count,
                "Face detected": sync_objects.image_capture_data.face_detected,
                "Forward Distance": sync_objects.hardware.ultrasonic.measure(),
                "Motor 1 Speed": sync_objects.hardware.motor_pair.m1.sensor_speed,
                "Motor 2 Speed": sync_objects.hardware.motor_pair.m2.sensor_speed,
                "Servo Horiz": sync_objects.hardware.servo_pair.horizontal.current,
                "Servo Vert": sync_objects.hardware.servo_pair.vertical.current,
            }
        }
        ws.send_json(message)
        await asyncio.sleep(1)

async def client_log_message_queue_worker(sync_objects, ws):    
    while True:
        msg = await sync_objects.client_log_message_queue.get()
        message = {
            "log": msg
        }
        ws.send_json(message)
        
async def websocket_handler(sync_objects, request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    sync_objects.loop.create_task(system_info_websocket_heartbeat(sync_objects, ws))
    sync_objects.loop.create_task(client_log_message_queue_worker(sync_objects, ws))

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            data = json.loads(msg.data)
            if "closeSocket" in data:
                await ws.close()
            elif "clientVideoConnected" in data:
                if data["clientVideoConnected"]:
                    sync_objects.allow_camera_capture.release()
                else:
                    sync_objects.allow_camera_capture.acquire()
            elif "command" in data:
                sync_objects.hardware_command_queue.put_nowait(data["command"])
            else:
                log.info("Unrecognized message: " + msg.data)
        elif msg.type == WSMsgType.ERROR:
            log.info('ws connection closed with exception %s' %
                  ws.exception())

    log.info('websocket connection closed')
    return ws

async def hardware_manager(sync_objects):
    while True:
        message = await sync_objects.hardware_command_queue.get()
        log.debug('received: %s' % (message))
        if message == "forward":
            sync_objects.hardware.motor_pair.accelerate(.1)
        elif message == "backward":
            sync_objects.hardware.motor_pair.accelerate(-.1) 
        elif message == "turnleft":
            sync_objects.hardware.motor_pair.bear_left(.1)
        elif message == "turnright":
            sync_objects.hardware.motor_pair.bear_right(.1)
        elif message == "brake":
            sync_objects.hardware.motor_pair.set_velocity(0)
        elif message == "panleft":
            sync_objects.hardware.servo_pair.pan_left()
        elif message == "panright":
            sync_objects.hardware.servo_pair.pan_right()
        elif message == "tiltup":
            sync_objects.hardware.servo_pair.tilt_up()
        elif message == "tiltdown":
            sync_objects.hardware.servo_pair.tilt_down()
        elif message == "center":
            sync_objects.hardware.servo_pair.center()
        #elif message == "autopiloton":
        #    auto_pilot.start()
        #    auto_pilot_on = True
        #elif message == "autopilotoff":
        #    auto_pilot.stop()
        #    auto_pilot_on = False
        else:
            log.debug('unknown message received: %s' % (message))

def create_web_application(sync_objects):
    module_dir = os.path.dirname(__file__)
    
    app = web.Application()
    app.router.add_get('/', partial(index, sync_objects))
    app.router.add_get('/video-feed', partial(video_feed, sync_objects))
    app.router.add_get('/sys-info-ws', partial(websocket_handler, sync_objects))
    app.router.add_static('/static/',
                      path=os.path.join(module_dir, "static", ""),
                      name='static')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(module_dir, "templates", "")))
    return app

async def create_http_server(loop, app):
    srv = await loop.create_server(app.make_handler(), 
                                   settings.http_server_address, settings.http_server_port)
    log.info('serving on ' + repr(srv.sockets[0].getsockname()))
    return srv

def main():
    from robot.utility.logging import console_log_handler, file_log_handler
    logger = logging.getLogger('')
    logger.addHandler(console_log_handler)
    logger.addHandler(file_log_handler)
    logger.setLevel(logging.DEBUG)
    
    loop = asyncio.get_event_loop()
    sync_objects = SyncObjects(loop)
    app = create_web_application(sync_objects)
    loop.create_task(hardware_manager(sync_objects))
    loop.create_task(camera_detect_worker(sync_objects))
    loop.run_until_complete(create_http_server(loop, app))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
