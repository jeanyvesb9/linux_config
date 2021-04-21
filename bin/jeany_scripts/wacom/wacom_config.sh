#!/bin/bash

# Written by Jean Yves Beaucamp - 2021
#
# To be run on .xsession, and as a systemd --user service with a udev rule call


# ================================================================================
# CONFIGURATION

# Set this to your generic device name. Find it by running:
#
# xsetwacom --list devices
#
# There will be multiple entries listed for the same device. For example: 
#   > xsetwacom --list devices
#   Wacom Intuos PT S 2 Pen stylus  	id: 8	type: STYLUS
#   Wacom Intuos PT S 2 Finger touch	id: 9	type: TOUCH
#   Wacom Intuos PT S 2 Pad pad     	id: 10	type: PAD
#
# In this case, you should set: DEVICE='Wacom Intuos PT S 2'
device='Wacom Intuos PT S 2'
# ================================================================================

if ! timeout 1s xset q &>/dev/null; then
    echo 'No X Session.'
    exit 1
fi

# Wait for up to 5 seconds for the device to show up
counter=0
while [ -z "$(xsetwacom --list devices)" ]; do
    if [ $counter -eq 11 ]; then
        echo 'No Wacom tabet connected.'
        exit 1
    fi
    sleep .5 #Wait 0.5 seccond
    counter=$((counter + 1))
done

id_stylus=$(xsetwacom --list | grep -i "$device" | grep -i "stylus" | awk '{print $(NF-2)}')
#id_touch=$(xsetwacom --list | grep -i "$device" | grep -i "touch" | awk '{print $(NF-2)}')
id_pad=$(xsetwacom --list | grep -i "$device" | grep -i "pad" | awk '{print $(NF-2)}')

# Set Stylus bindings
xsetwacom --set "$id_stylus" Button 2 "pan"
xsetwacom --set "$id_stylus" "PanScrollThreshold" 200


# Set Pad bindings
# For Wacom Intuos PT S 2:
#   -UL (Button 3): Switch-monitor script (through mouse b:10 keybinding on xbindkeys)
#   -UR (Button 9): Switch-to-VM script (through mouse b:11 keybinding on xbindkeys)
#   -LL (Button 1): Shift
#   -LR (Button 2): Control + z
xsetwacom --set "$id_pad" Button 3 10
xsetwacom --set "$id_pad" Button 9 11
xsetwacom --set "$id_pad" Button 1 "key shift"
xsetwacom --set "$id_pad" Button 2 "key control z"

# Set initial monitor binding to drawing area
. ~/bin/jeany_scripts/wacom/wacom_monitor_switch.sh --manual-config=0
