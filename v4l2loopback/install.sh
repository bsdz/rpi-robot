# run as root

chmod a+r v4l2loopback.ko
modprobe videodev
rmmod v4l2loopback
insmod ./v4l2loopback.ko video_nr=2
