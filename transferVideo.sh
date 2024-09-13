#!/bin/bash
# requires username as 1st positional argument and path to save folder as 2nd positional argument

cd "$(dirname "$0")"
path=$1@10.1.1.0:$2
echo "Started video transfer to ""$path"" at ""$(date +%H:%M:%S)"" "
rsync --recursive --times --compress --progress --exclude=".*"  vids/ "$path"
echo "transferVideo.sh Finished"
