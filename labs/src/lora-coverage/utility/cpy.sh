#!/bin/bash
# ------------------------------------------------------------
# This script copy micropython script
# Author: Marco Rainone
# Ver. 1.0, 2017/04/01
#
if [ "$#" -ne 2 ]; then
    echo "--------------------------------------------------------------------------------------"
    echo "Illegal number of parameters"
	echo "This script copy micropython script in flash."
    echo "Use: $0 <name_program> <dest>"
	echo "example:"
	echo "$0 rgb /flash"
	echo "copy rgb.py in root flash"
    echo "--------------------------------------------------------------------------------------"
	echo ""
	exit 1
fi
# example:
# ampy --port /dev/ttyUSB0 put tstmqttspeak.py /flash/tstmqttspeak.py
ampy --port /dev/ttyUSB0 put $1.py $2/$1.py
