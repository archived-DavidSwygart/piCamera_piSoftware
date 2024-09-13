#!/bin/bash
echo "git pull latest camera code"
cd "$(dirname "$0")"
git pull
echo "cam/update.sh finished"
