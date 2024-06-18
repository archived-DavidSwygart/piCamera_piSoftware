#!/bin/bash
#This script records a video 
#Arguments: $1:Name of Video, $2: Length (minutes), $3: Frames per second

export DISPLAY=:0

ans=$(echo "$2 * 60000" | bc)
now=$(date "+%F")
echo "Started recording at" $(date +%H:%M:%S)


rpicam-vid -t $ans --codec h264 --denoise off --level 4.2   -o $1"_"$HOSTNAME"_"$now.h264

echo "Finished for now..."
