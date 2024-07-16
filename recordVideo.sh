#!/bin/bash
#This is a simple wrapper that calls the python script capture_video.py
#Arguments: $1 = Length (seconds)

cd "$(dirname "$0")" #CD to directory of this script

v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0 #Turn on HDR video mode
python capture_video.py "$1" 
