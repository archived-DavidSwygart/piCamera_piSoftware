#!/usr/bin/python3
import time
import os
import sys
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder

os.environ["DISPLAY"] = ':0' 
duration = int(sys.argv[1])

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = H264Encoder(10000000)

picam2.start_preview(Preview.QTGL, width=800, height=480, x=0, y=0)
picam2.title_fields = ["ExposureTime", "AnalogueGain","Lux"]
picam2.start_encoder(encoder,  'test.h264')
picam2.start()

time.sleep(duration)

picam2.stop()
picam2.stop_encoder()
