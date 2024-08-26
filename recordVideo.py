#!/usr/bin/python3
from pprint import *
import time
import os
import sys

#This script assumes HDR is turned on. HDR must be turned on at terminal
#ON - v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0
#OFF -v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from libcamera import controls

#Turn of Info and warning logging
Picamera2.set_logging(Picamera2.ERROR)
os.environ["LIBCAMERA_LOG_LEVELS"]="3"

os.environ["DISPLAY"] = ':0' 

duration = 60*60*24
if len(sys.argv) > 1:
    if int(sys.argv[1])>0:
        duration = int(sys.argv[1])
print("duration = " + str(duration) + "s")

picam2 = Picamera2()

modeNum = 0
mode = picam2.sensor_modes[modeNum]
picam2.video_configuration.sensor.output_size = mode['size']
picam2.video_configuration.transform.hflip = True
picam2.video_configuration.transform.vflip = True
picam2.configure("video")

encoder = H264Encoder(
    bitrate=10000000,
    framerate=mode['fps']
    )

import datetime
vidName = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
output = FfmpegOutput(output_filename='vids/'+vidName+'.mp4')

picam2.start_preview(Preview.QTGL, width=800, height=480, x=0, y=0)
picam2.title_fields = ["ExposureTime", "AnalogueGain","Lux"]
picam2.start_encoder(
    encoder=encoder,
    output=output
    )
picam2.start()

time.sleep(duration)

picam2.stop()
picam2.stop_encoder()
