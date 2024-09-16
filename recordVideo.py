#!/usr/bin/python3
import os
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0") #turn on HDR
#os.system("v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0") #turn off HDR
os.environ["DISPLAY"] = ':0' 

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import warnings, signal, sys
import argparse, datetime, time

def endRecording(sig, frame):
    picam2.stop()
    if not args.noSave:
        picam2.stop_encoder()
    print('recordVideo.py finished')
    sys.exit(0)

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
parser.add_argument('--session', '-s', 
                    help='Name session, which determines the folder name in which the video will be saved defaults to date and time)'
                    )

args = parser.parse_args()

#Start PiCamera2
picam2 = Picamera2()

#Configure camera
print('configuring camera')
modeNum = 0
mode = picam2.sensor_modes[modeNum]
picam2.video_configuration.sensor.output_size = mode['size']
picam2.video_configuration.transform.hflip = True
picam2.video_configuration.transform.vflip = True
picam2.configure("video")

#Start preview window
print('Starting preview window')
picam2.start_preview(Preview.QTGL, width=800, height=480, x=0, y=0)
picam2.title_fields = ["ExposureTime", "AnalogueGain","Lux"]

# Set up encoder
if not args.noSave:
    print('Setting up H264 encoder')
    encoder = H264Encoder(
        bitrate=10000000,
        framerate=mode['fps']
        )
    scriptPath = os.path.dirname(__file__)
    hostname = os.uname().nodename
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    if args.session is None:
        session = now
    else:
        session = args.session

    saveDirectory = scriptPath + '/vids/' + session + '/' + hostname

    if os.path.exists(saveDirectory):
        warnings.warn("directory already exists for "+session+". Other videos could already be in "+saveDirectory)
    else:
        os.makedirs(saveDirectory)

    saveFile = saveDirectory + '/' + now + '.mp4'
    print('SavingFile as '+saveFile)
    
    output = FfmpegOutput(output_filename=saveFile)
    picam2.start_encoder(
        encoder=encoder,
        output=output
        )

#Record for specified duration
picam2.start()
signal.signal(signal.SIGINT, endRecording)
signal.signal(signal.SIGTERM, endRecording)
print('waiting for a duration of '+str(args.duration) + ' seconds')
time.sleep(args.duration)
endRecording(0,None)

