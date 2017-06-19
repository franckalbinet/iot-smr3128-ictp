#!/bin/bash
# ------------------------------------------------------------
# This script copy micropython script
# Author: Marco Rainone
# Ver. 1.0, 2017/04/01
#
if [ "$#" -ne 2 ]; then
    echo "--------------------------------------------------------------------------------------"
    echo "Illegal number of parameters"
	echo "This script read micropython script in flash."
    echo "Use: $0 <name_program> <dest>"
	echo "example:"
	echo "$0 /flash rgb.py"
	echo "read rgb.py in root flash"
    echo "--------------------------------------------------------------------------------------"
	echo ""
	exit 1
fi
# original
# ampy --port /dev/ttyUSB0 get $1/$2 $2
# mod 18/05
# https://github.com/dhylands/rshell
rshell -p /dev/ttyUSB0 cp $1/$2 $2
