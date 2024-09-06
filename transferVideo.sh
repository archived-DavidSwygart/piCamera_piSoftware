#!/bin/bash
# requires path to behavior server as 1st positional argument

cd "$(dirname "$0")"
echo "Started video transfer to ""$1"" at ""$(date +%H:%M:%S)"" "
rsync --recursive --times --compress --progress vids "$1"
