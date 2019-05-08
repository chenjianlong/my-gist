#!/bin/sh
# file disable_touchpad.sh
# author Jianlong Chen <jianlong99@gmail.com>
# date 2013-07-18

id=$(xinput list | grep TouchPad | sed -n 's#.*id=\([0-9]\+\).*#\1#p')
xinput set-prop ${id} "Device Enabled" 0
