'''
Created on 23 Sep 2017

@author: pi
'''
from aiohttp import web, WSMsgType, ClientError
import aiohttp_jinja2
import jinja2
import asyncio
from threading import Thread
import time, uuid
import cv2
import os
import json
import async_timeout

import robot.settings as settings
from robot.hardware.system import SystemInfo

from robot.hardware.motor import MotorPair
from robot.hardware.servo import ServoPair
from robot.hardware.ultrasonic import Ultrasonic
#from robot.autopilot import AutoPilot

from robot.utility.logger import Logger
log = Logger("Main").get_log()

loop = asyncio.get_event_loop()
allow_camera_capture = asyncio.Semaphore(value=0, loop=loop)
client_log_message_queue = asyncio.Queue()
client_image_queue = asyncio.Queue(maxsize=1)
client_image_queue_lock = asyncio.Lock()

image_capture_count = 0

app = web.Application()

motor_pair = MotorPair()
servo = ServoPair()
ultrasonic = Ultrasonic()
#auto_pilot = AutoPilot()

def process_command(message):
    log.debug('received: %s' % (message))
    if message == "forward":
        motor_pair.accelerate(10)
    elif message == "backward":
        motor_pair.accelerate(-10) 
    elif message == "turnleft":
        motor_pair.bear_left(-10)
    elif message == "turnright":
        motor_pair.bear_right(-10)
    elif message == "brake":
        motor_pair.set_velocity(0)
    elif message == "panleft":
        servo.pan_left()
    elif message == "panright":
        servo.pan_right()
    elif message == "tiltup":
        servo.tilt_up()
    elif message == "tiltdown":
        servo.tilt_down()
    elif message == "center":
        servo.center()
    #elif message == "autopiloton":
    #    auto_pilot.start()
    #    auto_pilot_on = True
    #elif message == "autopilotoff":
    #    auto_pilot.stop()
    #    auto_pilot_on = False
    else:
        log.debug('unknown message received: %s' % (message))

#     message = {
#         "status": {
#             "m1Speed": self.motor_pair.m1.get_velocity(),
#             "m2Speed": self.motor_pair.m2.get_velocity(),
#             "servoHoriz": self.servo.horizontal.current,
#             "servoVert": self.servo.vertical.current,
#         }
#     }

async def camera_detect_worker():
    face_cascade = cv2.CascadeClassifier(os.path.join(settings.haar_cascade_dir, "haarcascade_frontalface_alt.xml"))
    eye_cascade = cv2.CascadeClassifier(os.path.join(settings.haar_cascade_dir, "haarcascade_eye.xml"))
    smile_cascade = cv2.CascadeClassifier(os.path.join(settings.haar_cascade_dir, "haarcascade_smile.xml"))
    sF = 1.05
    
    await allow_camera_capture.acquire()
    log.info("Capturing camera...")
    await client_log_message_queue.put("Server capturing camera")
    video_capture = cv2.VideoCapture(settings.video_capture_device)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, settings.video_width)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.video_height)
    global image_capture_count
    
    while True:
        success, image = video_capture.read()
        if success:
            image_capture_count += 1
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=sF,
                minNeighbors=8,
                minSize=(55, 55),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            #if faces:
            #    await client_log_message_queue.put(repr(faces))
            # ---- Draw a rectangle around the faces
        
             
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = image[y:y+h, x:x+w]
         
                smile = smile_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor= 1.7,
                    minNeighbors=22,
                    minSize=(25, 25),
                    flags=cv2.CASCADE_SCALE_IMAGE
                    )
         
                # Set region of interest for smiles
                for (x, y, w, h) in smile:
                    cv2.putText(image,"Smile detected", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                    cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)
            
        
            with (await client_image_queue_lock):
                image_jpeg_bytes = cv2.imencode('.jpg', image)[1].tobytes()
                if client_image_queue.full():
                    client_image_queue.get_nowait()
                client_image_queue.put_nowait(image_jpeg_bytes)
        
        await asyncio.sleep(.2)


@aiohttp_jinja2.template('index.html')
async def index(request):

    if settings.video_source == "server_mjpeg_stream":
        allow_camera_capture.release()
    return dict({"video_source": settings.video_source})


async def video_feed(request, timeout=10):
    """Stream a stream to aiohttp web response."""
    response = web.StreamResponse()
    response.content_type = 'multipart/x-mixed-replace;boundary=ffserver'
    await response.prepare(request)

    try:
        while True:
            with async_timeout.timeout(timeout, loop=loop):
                data = await client_image_queue.get()

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



async def system_info_websocket_heartbeat(ws):
    si = SystemInfo()
    global image_capture_count
    while True:
        message = {
            "status": {
                "CPU Temp": si.cpu_temperature(),
                "GPU Temp": si.gpu_temperature(),
                "Core Volt": si.core_voltage(),
                "CPU Load": si.cpu_load(),
                "Images #": image_capture_count,
                "Forward Distance": ultrasonic.measure()
            }
        }
        ws.send_json(message)
        await asyncio.sleep(1)

async def client_log_message_queue_worker(ws):    
    while True:
        msg = await client_log_message_queue.get()
        message = {
            "log": msg
        }
        ws.send_json(message)
        
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    loop.create_task(system_info_websocket_heartbeat(ws))
    loop.create_task(client_log_message_queue_worker(ws))

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            data = json.loads(msg.data)
            if "closeSocket" in data:
                await ws.close()
            elif "clientVideoConnected" in data:
                if data["clientVideoConnected"]:
                    allow_camera_capture.release()
                else:
                    allow_camera_capture.acquire()
            elif "command" in data:
                process_command(data["command"])
            else:
                log.info("Unrecognized message: " + msg.data)
        elif msg.type == WSMsgType.ERROR:
            log.info('ws connection closed with exception %s' %
                  ws.exception())

    log.info('websocket connection closed')

    return ws



module_dir = os.path.dirname(__file__)

app.router.add_get('/', index)
app.router.add_get('/video-feed', video_feed)
app.router.add_route('GET', '/sys-info-ws', websocket_handler)
app.router.add_static('/static/',
                  path=os.path.join(module_dir, "static", ""),
                  name='static')

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(module_dir, "templates", "")))
#web.run_app(app, host='0.0.0.0', port=8080)

async def init(loop):
    handler = app.make_handler()
    srv = await loop.create_server(handler, '0.0.0.0', settings.http_server_port)
    log.info('serving on ' + repr(srv.sockets[0].getsockname()))
    return srv

def main():
    
    loop.create_task(camera_detect_worker())
    loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

main()
