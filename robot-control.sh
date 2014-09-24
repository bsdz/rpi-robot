#!/bin/bash
# streaming: http://phoboslab.org/log/2013/09/html5-live-video-streaming-via-websockets

if [ "$UID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

PATH=/sbin:/usr/sbin:/bin:/usr/bin

V4L2CTL_PATH=/usr/bin/v4l2-ctl
WEBSERVER_PATH=./webserver.py
FACEDETECT_PATH=./facedetect.py
NODEJS_PATH=./node-v0.10.2-linux-arm-pi/bin/node
SERVOD_PATH=./ServoBlaster-User/servod
SERVOD_OPTS="--p1pins=24,26 --idle-timeout=2000"

USE_FACE_DETECT=false

res=0

function wait_tcp () {
    local nc op host port failed limit tries
    limit=100
    host=$1
    port=$2
    op="open"
 
    echo -n "Wait for TCP $host:$port.."

    tries=0
    while true; do
        if [[ $limit -gt 0 && $tries -ge $limit ]]; then
            failed=1
            break
        fi

        timeout --foreground 0.5 bash -c \
            "echo >\"/dev/tcp/$host/$port\"" >&/dev/null

        ret=$?
        tries=$((tries + 1))
        if [ $op = "close" -a "$ret" -ne 0 ]; then
            break
        fi
        if [ $op = "open" -a "$ret" -eq 0 ]; then
            break
        fi
        sleep 1
        echo -n "."
    done

    if [[ -z "$failed" ]]; then
        echo "done"
    else
        echo "failed"
        exit 1
    fi
}
 
function stop_all() {
    echo Stopping all processes..
    killall servod
    killall node
    killall webserver.py
    killall avconv
    killall facedetect.py
    #killall v4l2-ctl
}

function unregister_modules() {
    modprobe -r bcm2835-v4l2
    rmmod v4l2loopback
}

function register_modules() {
    echo "registering onboard camera (/dev/video0).."
    modprobe bcm2835-v4l2
    $V4L2CTL_PATH --set-ctrl video_bitrate=100000
    $V4L2CTL_PATH --set-fmt-video=width=320,height=240,pixelformat=5
    
    echo "registering loopback video (/dev/video2).."
    modprobe videodev
    insmod ./v4l2loopback/v4l2loopback.ko video_nr=2
  
    echo "registering servoblaster (/dev/servoblaster).."
    $SERVOD_PATH $SERVOD_OPTS >/dev/null
}

function check_status() {
    [ -e /dev/servoblaster ] || res=4
    $V4L2CTL_PATH --list-devices    
}

# h264: avconv: h264, v4l2: 4
# mjpeg: avconv: mjpeg, v4l2: 5
function start_all() {
    unregister_modules
    register_modules
    
    echo "starting node mpeg multicaster.."
    $NODEJS_PATH jsmpeg/stream-server.js SeCrEt 8082 8084 &
    
    echo "starting web server.."
    $WEBSERVER_PATH &

    STREAM_SOURCE_DEVICE=/dev/video0
    if $USE_FACE_DETECT; then
        echo "starting face detection service.."
        STREAM_SOURCE_DEVICE=/dev/video2
        LD_LIBRARY_PATH=./opencv-patched/lib/ $FACEDETECT_PATH &
    fi

    #LD_LIBRARY_PATH=./opencv-patched/lib/ $FACEDETECT_PATH &
    
    echo "sleep to allow for jobs to start.."
    wait_tcp 127.0.0.1 8082 # strean server - video
    wait_tcp 127.0.0.1 8084 # stream server - websocket
    wait_tcp 127.0.0.1 9093 # web server
    sleep 10
    
    echo "starting avconv stream converter.."
    avconv -s 320x240 -r 5 -f video4linux2 -i $STREAM_SOURCE_DEVICE -f mpeg1video -b 100k -r 30 -an -loglevel quiet http://127.0.0.1:8082/SeCrEt/320/240/ &    
    
    # alternative streaming methods
    #$V4L2CTL_PATH --stream-mmap=3 --stream-to=- | avconv -f mjpeg -i pipe:0 -f mpeg1video -b 100k -r 30 -an -loglevel quiet http://127.0.0.1:8082/rfvgy7/320/240/ &
    #raspivid -t 999999 -fps 15 -vf -w 320 -h 240 -o - | avconv -f h264 -i pipe:0 -f mpeg1video -b 500k -r 25 http://127.0.0.1:8082/rfvgy7/320/240/
}

case "$1" in
    start)
        start_all 
        ;;
    restart|reload|force-reload)
        stop_all
        start_all
        ;;
    stop)
        stop_all
        ;;
    status)
        check_status
        ;;
    register)
        register_modules
        ;;
    unregister)
        unregister_modules
        ;;
    *)
        echo "Usage: robot-control.sh [start|stop|restart|status|register|unregister]" >&2
        res=3
        ;;
esac

exit $res

