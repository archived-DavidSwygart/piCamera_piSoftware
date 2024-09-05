#!/usr/bin/python3
import os
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0") #turn on HDR
#os.system("v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0") #turn off HDR
os.environ["DISPLAY"] = ':0' 

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import argparse, datetime, time

#Turn off Info and warning logging
Picamera2.set_logging(Picamera2.ERROR)
os.environ["LIBCAMERA_LOG_LEVELS"]="3"

#Parse recording settings
parser = argparse.ArgumentParser(description='Display and record video.')
parser.add_argument('--duration', '-d', 
                    type=int, 
                    help='Recording duration in seconds (default=86400s)',
                    default='86400')
parser.add_argument('--noSave', '-n', 
                    action='store_true',
                    help='No file is saved. Screen still displays the video')

args = parser.parse_args()

#Start PiCamera2
picam2 = Picamera2()

#Configure camera
modeNum = 0
mode = picam2.sensor_modes[modeNum]
picam2.video_configuration.sensor.output_size = mode['size']
picam2.video_configuration.transform.hflip = True
picam2.video_configuration.transform.vflip = True
picam2.configure("video")

#Start preview window
picam2.start_preview(Preview.QTGL, width=800, height=480, x=0, y=0)
picam2.title_fields = ["ExposureTime", "AnalogueGain","Lux"]

# Set up encoder
if not args.noSave:
    encoder = H264Encoder(
        bitrate=10000000,
        framerate=mode['fps']
        )
    scriptPath = os.path.dirname(__file__)
    hostname = os.uname().nodename
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    saveFile = scriptPath+'/vids/'+hostname+'_'+now+'.mp4'
    output = FfmpegOutput(output_filename=saveFile)
    picam2.start_encoder(
        encoder=encoder,
        output=output
        )

#Record for specified duration
picam2.start()
time.sleep(args.duration)
picam2.stop()
if not args.noSave:
    picam2.stop_encoder()
